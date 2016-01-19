import feedparser
import codecs
import MySQLdb
import time

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

def add_entries(data):
    db = MySQLdb.connect("localhost","root","5961", "news")
    cursor = db.cursor()

    fh = codecs.open("test", "w", "utf-8")
    for article in data.entries:
        time.sleep(1)
        identifier = article.title + article.published
        title = article.title
        fecha = article.published
        newsp = "ELDIARIO.ES"
        content = article.description

        title.replace("'", r"\'")
        content.replace("'", r"\'")
        title = title.encode("ascii", "ignore")
        content = content.encode("ascii", "ignore")

        fh.write("IDENTIFIER: " + identifier + "\n\n")
        fh.write("TITLE: " + title + "\n\n")
        fh.write("FECHA: " + fecha + "\n\n")
        fh.write("newsp: " + newsp + "\n\n")
        fh.write("CONTENT: " + content + "\n\n")
        fh.write("-----\n")

        sql = "INSERT INTO NEWSTABLE(ID, TITLE, FECHA, NEWSPAPER, CONTENT) \
VALUES ('%s', '%s', '%s', '%s', '%s')" % (title, identifier, fecha, newsp, content)
        try:
            cursor.execute(sql)
            db.commit()
            print("TO BIEN")
        except MySQLdb.ProgrammingError, e:
            print 'There was a MySQL warning.  This is the info we have about it: %s' %(e)
            print("NO se pudo subir datos")

    db.close()

feed = read_rss('http://eldiario.es.feedsportal.com/rss')
write_feed("kk.html", feed)
add_entries(feed)
