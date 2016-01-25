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
    i     = 1
    for line in sfile:
        line = line.strip()
        if line[0] == "#":
            continue
        codes[line] = i
        i += 1
    sys.stderr.write(str(codes) + "\n")
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
def add_entries(data, category):

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
        newsp   = "ELDIARIO"
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
        #sql =  "INSERT INTO search_news_articles (identifier, title, pubdate, source, language, link, content, category_id) \
        #        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') \
        #       SELECT * FROM (SELECT '%s') AS tmp \
        #       WHERE NOT EXISTS ( \
        #            SELECT identifier FROM search_news_articles WHERE identifier = '%s' \
        #       );" % ( identifier, title, date, newsp, "ESP", link, content, category, identifier, identifier)
        sql = "INSERT INTO search_news_articles (identifier, title, pubdate, source, language, link, content, category) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % ( identifier, title, date, newsp, "ESP", link, content, category)

        try:
            cursor.execute(sql)
            db.commit()
            sys.stderr.write('Adding article to database: ' + identifier + '  ok\n')
        except MySQLdb.ProgrammingError, e:
            sys.stderr.write('Adding article to database: ' + identifier + '  not ok\n')
            sys.stderr.write('\tWarning %s' %(e) )

    db.close()


# ---------------------------------------------
'''
This function reads the feeds with their category. It returns a list of tuples.
'''
def read_feeds(filename):
    my_feeds = list()
    fd = open(filename, "r")
    for line in fd:
        line      = line.strip()
        feed_elem = line.split()
        feed_tup  = (feed_elem[0], feed_elem[1])
        my_feeds.append(feed_tup)
        print(feed_tup)
    return(my_feeds)


def add_categories(cat):
    # CONNECT TO DATABASE
    db     = MySQLdb.connect("localhost","root","5961", "news")
    cursor = db.cursor()

    # UTF8 THINGS
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    sql =  "INSERT INTO search_news_category (category) \
           SELECT * FROM (SELECT '%s') AS tmp \
           WHERE NOT EXISTS ( \
                SELECT category FROM search_news_category WHERE category = '%s' \
           );" % (cat, cat)
    try:
        cursor.execute(sql)
        db.commit()
        sys.stderr.write('Adding category to database: ' + cat + '  ok\n')
    except MySQLdb.ProgrammingError, e:
        sys.stderr.write('Adding category to database: ' + cat + '  not ok\n')
        sys.stderr.write('\tWarning %s' %(e) )

    db.close()



# ---------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------

# GET SCRIPT PATH
script_path = os.path.realpath(__file__)
script_path = script_path.replace("rss_getter.py", "")

# GET FEEDS WITH CATEGORIES
feed_path   = script_path + "feeds.tbl"
all_feeds  = read_feeds(feed_path)

# UPLOAD FEEDS TO DB
for feed in all_feeds:
    feed_obj = read_rss(feed[0])
    add_categories(feed[1])
    add_entries(feed_obj, feed[1])
