import feedparser
import codecs

def write_feed(file, data):
    fh = codecs.open(file, "w", "utf-8")

    fh.write("<html>\n<meta charset=\"UTF-8\"> ")
    fh.write("<h1>" + data.feed.title + "</h1>")

    fh.write("<h1> TAGS: \n<p>" + data.feed.tags + "</p></h1>")
    for post in data.entries:
        fh.write("<h2>" + post.title + "</h1>")
        fh.write ("<p><a href=\"" + post.link + "\">Source </a></p>")
        fh.write("<p>" + post.published + "</p>")
        fh.write("<p>" + post.description + "</p>\n")

        fh.write("</html>")

def read_rss(link):
    d = feedparser.parse(link)
    return(d)



feed = read_rss('http://eldiario.es.feedsportal.com/rss')
write_feed("kk.html", feed)
