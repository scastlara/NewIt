# ---------------------------------------------
# MODULES
# ---------------------------------------------
import feedparser
import codecs
import MySQLdb
import time
import sys
import os


# ---------------------------------------------
# FUNCTIONS
# ---------------------------------------------

# ---------------------------------------------
'''
This function is for debugging/development. It prints the feeds to an html file.
'''
def write_feed(file, data):

    fh = codecs.open(file, "w", "utf-8")

    fh.write("<html>\n<meta charset=\"UTF-8\"> ")

    for post in data.entries:
        fh.write("<h2>" + post.title + "</h1>")
        fh.write ("<p><a href=\"" + post.link + "\">Source </a></p>")
        fh.write("<p>" + post.published + "</p>")
        fh.write("<p>" + post.description + "</p>\n")

        fh.write("</html>")


# ---------------------------------------------
'''
Function that downloads and parses de XML from the feed
'''
def read_rss(link):
    d = feedparser.parse(link)
    return(d)


# ---------------------------------------------
'''
Changes the date to a format suitable for MySQL
'''
def date_changer(date):
	month_dict={ 'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
	date = date.split(" ")
	sergio_date = date[4].split(":")[0] + date[4].split(":")[1]
	new_date = date[3]+"-"+month_dict[date[2]]+"-"+date[1]+" "+date[4]
	return (new_date,sergio_date)


# ---------------------------------------------
'''
Function that reads all the "allowed" sources and assigns a number to them
for the article "identifier"
'''
def read_sources():
    codes = dict()
    script_path = os.path.realpath(__file__)
    script_path = script_path.replace("rss_getter.py", "")
    source_file = script_path + "sources.txt"
    sfile = open(source_file, "r")
    i     = 0
    for line in sfile:
        line = line.strip()
        if line[0] == "#":
            continue
        codes[line] = i
        i += 1
    sys.stderr.write(str(codes))
    return(codes)


# ---------------------------------------------
'''
This hashing function creates a "unique" ID for each article/story
'''
def get_ID(title, source, date, source_codes):
    title = title.encode("ascii", "ignore")
    words = title.split()
    title_code = int()
    max_i = 10
    prime_nums = [2, 3, 5, 7, 11, 13, 17, 19, 23, 27]
    i     = 0
    for word in words:
        if i < max_i:
            title_code += ord(word[0]) * prime_nums[i]
            i += 1
        else:
            break

    sys.stderr.write("Source: " + str(source_codes[source]) + " Title: " + str(title_code) + " Date:" + str(date) + "\n")
    final_code = str()
    final_code = str(source_codes[source]) + str(title_code) + str(date)
    return(final_code)


# ---------------------------------------------
'''
Uploads the News/articles to our MySQL database. Right now it uses the module MySQLdb.
We may need to change it to PyMySQL, depending on the configuration of GELPI's server.
It is a very big function. It needs refactoring.
'''
def add_entries(data):

    # CONNECT TO DATABASE
    db     = MySQLdb.connect("localhost","root","5961", "news")
    cursor = db.cursor()

    # UTF8 THINGS
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # READ FEED SOURCES
    source_codes = read_sources()

    for article in data.entries:
        time.sleep(1)
        title   = article.title
        date   = article.published
        newsp   = "ELDIARIO.ES"
        content = article.description
        link    = article.link

        # (formatted_date, hour+minutes)
        date_tuple = date_changer(date)
        date = date_tuple[0]

        # GET ID FOR DATABASE
        identifier = get_ID(title, newsp, date_tuple[1], source_codes)

        # REMOVE SINGLE QUOTES
        title   = title.replace("'", "")
        content = content.replace("'", "")

        # SQL QUERY TO ADD DATA TO DB
        sql = "INSERT INTO search_news_notisiario (identifier, title, pubdate, source, language, link, content) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ( identifier, title, date, newsp, "ESP", link, content)

        try:
            cursor.execute(sql)
            db.commit()
            sys.stderr.write('Adding article to database: ' + identifier + '  ok\n')
        except MySQLdb.ProgrammingError, e:
            sys.stderr.write('Adding article to database: ' + identifier + '  not ok\n')
            sys.stderr.write('\tWarning %s' %(e) )

    db.close()


# ---------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------

feed = read_rss('http://eldiario.es.feedsportal.com/rss')
write_feed("kk.html", feed)
add_entries(feed)
