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

def get_ID(title, source, date):
    title = title.encode("ascii", "ignore")
    words = title.split()

    source_codes = { 'ELDIARIO.ES':001  }
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
    print(title_code)

def add_entries(data):
    db     = MySQLdb.connect("localhost","root","5961", "news")
    cursor = db.cursor()
    db.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    fh = codecs.open("test", "w", "utf-8")

    fileout = codecs.open("culo", "w", "utf-8")

    for article in data.entries:
        time.sleep(1)
        identifier = article.title + article.published
        title   = article.title
        fecha   = article.published
        newsp   = "ELDIARIO.ES"
        content = article.description

        # GET ID FOR DATABASE
        get_ID(title, newsp, fecha)
        title = title.replace("'", "")
        content=content.replace("'", "")

        print(title)
        #title = title.encode("ascii", "ignore")
        #content = content.encode("ascii", "ignore")

        fh.write("IDENTIFIER: " + identifier + "\n\n")
        fh.write("TITLE: " + title + "\n\n")
        fh.write("FECHA: " + fecha + "\n\n")
        fh.write("newsp: " + newsp + "\n\n")
        fh.write("CONTENT: " + content + "\n\n")
        fh.write("-----\n")

        sql = "INSERT INTO NEWSTABLE(ID, TITLE, FECHA, NEWSPAPER, CONTENT) \
VALUES ('%s', '%s', '%s', '%s', '%s')" % (title, identifier, fecha, newsp, content)
        fileout.write(sql)
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
