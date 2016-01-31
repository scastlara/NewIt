'''This is a simple script that uploads feeds and categories to the DB.'''

import sys
import MySQLdb

try:
    filename = sys.argv[1]
except Exception as e:
    raise Exception("Give me the feeds.tbl file as a command line argument.")

db     = MySQLdb.connect("localhost","root","5961", "news")
cursor = db.cursor()

db.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

fd = open(filename, "r")

for line in fd:
    line = line.strip()
    if line[0] == "#":
        continue
    link, category, sourcename = line.split("|")

    sql = "INSERT INTO  search_news_sources (link, name, category) \
           VALUES ('%s', '%s', '%s') \
           ON DUPLICATE KEY UPDATE link=link;" % (link, category, sourcename)
    try:
        cursor.execute(sql)
        db.commit()
        sys.stderr.write("Adding source to DB:\n%s\n%s\n%s\n\n" % (link, sourcename, category))
    except Exception as e:
        db.rollback()
        raise Exception("Can't upload data to database for some reason %s" % e)
