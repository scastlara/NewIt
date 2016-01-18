import feedparser
import codecs
import MySQLdb

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
    db = MySQLdb.connect("localhost","testuser","qwerty", "news")
    cursor = db.cursor()

    #sql = """CREATE TABLE NEWS (
    #ID  CHAR(100) NOT NULL,
    #FECHA  CHAR(20),
    #NEWSPAPER CHAR(20),
    #CONTENT CHAR(10000))"""

    #try:
    #    cursor.execute(sql)
    #    db.commit()
    #    print("TABLA CREADA")
    #except:
    #    db.rollback()
    #    print("ERRORRRRR DB ERROR")

    for article in data.entries:
        identifier = "hola"
        fecha = "12"
        newsp = "ELDIARIO.ES"
        content = article.description

        sql = "INSERT INTO NEWSTABLE(ID, \
FECHA, NEWSPAPER, CONTENT) \
VALUES ('%s', '%s', '%s', '%s')" % (identifier, fecha, newsp, content)
        try:
            cursor.execute(sql)
            print("TO BIEN")
        except:
            db.rollback()
            print("NO se pudo subir datos")

    db.close()

feed = read_rss('http://eldiario.es.feedsportal.com/rss')
write_feed("kk.html", feed)
add_entries(feed)
