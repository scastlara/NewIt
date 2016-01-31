# ---------------------------------------------
# MODULES
# ---------------------------------------------
import feedparser
import codecs
import MySQLdb
import datetime
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
    new_date = date[3]+"-"+month_dict[date[2]]+"-"+date[1]+" "+date[4]
    return new_date


# ---------------------------------------------
'''
Uploads the News/articles to our MySQL database. Right now it uses the module MySQLdb.
We may need to change it to PyMySQL, depending on the configuration of GELPI's server.
It is a very big function. It needs refactoring.
'''
def add_entry(feed, category, source, language):
    db     = MySQLdb.connect("localhost","root","5961", "news")
    cursor = db.cursor()
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    for article in feed.entries:
        title   = article.title
        date    = article.published
        content = article.description
        link    = article.link
        date    = date_changer(date)

        # REMOVE SINGLE QUOTES
        title   = title.replace("'", "")
        content = content.replace("'", "")

        sql = "INSERT INTO  search_news_article (title, pubdate, source, language, link, content, category) \
               VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s') \
               ON DUPLICATE KEY UPDATE link=link;" % (title, date, source, language, link, content, category)

        try:
            cursor.execute(sql)
            db.commit()
            sys.stderr.write('# Adding article to database: ' + link + '  ok\n')
            sys.stderr.write('# \tdate: %s\n# \tsource: %s\n# \tcategory: %s\n\n' % (date, source, category))
        except MySQLdb.Error as e:
            db.rollback()
            sys.stderr.write('Adding article to database: ' + link + '  not ok\n')
            sys.stderr.write('# \tdate: %s\n# \tsource: %s\n# \tcategory: %s\n\n' % (date, source, category))
            sys.stderr.write('#\n \tWarning %s\n' %(e) )

    db.close()


# ---------------------------------------------
'''
This function reads the feeds with their category. It returns a list of tuples.
(link, category, source, language)
'''
def read_feeds(database, cursor):
    sql = "SELECT * FROM search_news_feed"

    cursor.execute(sql)
    results = cursor.fetchall()
    feeds = list()
    for row in results:
        feeds.append(row)
    return(feeds)


# ---------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------
def main():

    # CONNECT TO DATABASE
    db     = MySQLdb.connect("localhost","root","5961", "news")
    cursor = db.cursor()

    # UTF8 THINGS
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # GET FEEDS
    all_feeds  = read_feeds(db, cursor)

    # UPLOAD FEEDS TO DB
    for feed in all_feeds:
        feed_obj = read_rss(feed[0])
        # Need to check if feed is correct!!
        # (feedobject, category, source, language)
        add_entry(feed_obj, feed[1], feed[2], feed[3])


while True:
    sys.stderr.write("\n## STARTING JOB AT %s\n" % datetime.datetime.now().time())
    main()
    time.sleep(7200)
    sys.stderr.write("\n# ----- \n")
