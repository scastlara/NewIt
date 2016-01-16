import feedparser
import codecs

d = feedparser.parse('http://eldiario.es.feedsportal.com/rss')
fh = codecs.open("kk.html", "w", "utf-8")

fh.write("<html>\n<meta charset=\"UTF-8\"> ")
for post in d.entries:

    fh.write("<h1>" + post.title + "</h1>")
    fh.write ("<p><a href=\"" + post.link + "\">Source </a></p>")
    fh.write("<p>" + post.published + "</p>")
    fh.write("<p>" + post.description + "</p>\n")

fh.write("</html>")
