import feedparser
import codecs
import MySQLdb
import time
import sys

def write_feed(file, data):
    fh = codecs.open(file, "w", "utf-8")

    fh.write("<html>\n<meta charset=\"UTF-8\"> ")

    for post in data.entries:
        fh.write("<h2>" + post.title + "</h1>")
        fh.write ("<p><a href=\"" + post.link + "\">Source </a></p>")
        fh.write("<p>" + post.published + "</p>")
        fh.write("<p>" + post.description + "</p>\n")

        fh.write("</html>")

def read_rss(link):
    d = feedparser.parse(link)
    return(d)


def date_changer(date):
	month_dict={ 'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
	date = date.split(" ")
	sergio_date = date[4].split(":")[0] + date[4].split(":")[1]
	new_date = date[3]+"-"+month_dict[date[2]]+"-"+date[1]+" "+date[4]
	return (new_date,sergio_date)


def get_ID(title, source, date):
    title = title.encode("ascii", "ignore")
    words = title.split()

    source_codes = { 'ELDIARIO.ES': 1  }
    title_code = int()
    max_i = 10
    i     = 0
    for word in words:
        if i < max_i:
            title_code += ord(word[0])
            i += 1
        else:
            break

    final_code = str()
    final_code = str(source_codes[source]) + str(title_code) + str(date)
    return(final_code)

def add_entries(data):

    # CONNECT TO DATABASE
    db     = MySQLdb.connect("localhost","root","5961", "news")
    cursor = db.cursor()

    # UTF8 THINGS
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    for article in data.entries:
        time.sleep(1)
        title   = article.title
        date   = article.published
        newsp   = "ELDIARIO.ES"
        content = article.description

        # (formatted_date, hour+minutes)
        date_tuple = date_changer(date)
        date = date_tuple[0]

        # GET ID FOR DATABASE
        identifier = get_ID(title, newsp, date_tuple[1])

        # REMOVE SINGLE QUOTES
        title   = title.replace("'", "")
        content = content.replace("'", "")

        # SQL QUERY TO ADD DATA TO DB
        sql = "INSERT INTO NEWSTABLE(ID, TITLE, FECHA, NEWSPAPER, CONTENT) \
VALUES ('%s', '%s', '%s', '%s', '%s')" % ( identifier, title, date, newsp, content)

        try:
            cursor.execute(sql)
            db.commit()
            sys.stderr.write('Adding article to database: ' + identifier + '  ok\n')
        except MySQLdb.ProgrammingError, e:
            sys.stderr.write('Adding article to database: ' + identifier + '  not ok\n')
            sys.stderr.write('\tWarning %s' %(e) )

    db.close()


# FUNCTION CALLS TO TEST
feed = read_rss('http://eldiario.es.feedsportal.com/rss')
write_feed("kk.html", feed)
add_entries(feed)
