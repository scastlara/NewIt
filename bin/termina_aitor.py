#####################################
#  Las importaciones son buenas porque importas lo que produces
#####################################

import codecs
import MySQLdb
import datetime
import time
import sys
import os

#####################################
#  La columna link de search_news_articles (PK) es article en search_news_bookmark (SK) 
#####################################


#####################################
#  This program returns a dictionary in which the key is the link of the article and the value is the pubdate in search_news_articles
#####################################
def get_articles():

	artdate = {}
	# open a database connection
	# be sure to change the host IP address, username, password and database name to match your own
	connection = MySQLdb.connect (host = "frmc.mmb.pcb.ub.es", user = "dbw13", passwd = "dbw2016", db = "DBW13")

	# prepare a cursor object using cursor() method
	cursor = connection.cursor ()

	# execute the SQL query using execute() method.
	cursor.execute ("select * from search_news_article;")

	# fetch all of the rows from the query
	data = cursor.fetchall ()

	# charge the dictionary
	for row in data :
		
		artdate[row[0]] = row[1]

	# close the cursor object
	cursor.close ()

	# close the connection
	connection.close ()

	# return the dictionary with the link as key and the date as value
	return artdate
	
	# exit the program
	sys.exit()

#print(get_articles())

#####################################
#  This program returns a list with the link with all the links (article field) in the bookm search_news_bookmark
#####################################
def get_bookmarks():

	bookmarked = list()
	# open a database connection
	# be sure to change the host IP address, username, password and database name to match your own
	connection = MySQLdb.connect (host = "frmc.mmb.pcb.ub.es", user = "dbw13", passwd = "dbw2016", db = "DBW13")

	# prepare a cursor object using cursor() method
	cursor = connection.cursor ()

	# execute the SQL query using execute() method.
	cursor.execute ("select * from search_news_bookmark;")

	# fetch all of the rows from the query
	data = cursor.fetchall ()

	# charge the dictionary
	for row in data :
		bookmarked.append(row[2])

	# close the cursor object
	cursor.close ()

	# close the connection
	connection.close ()

	# return the dictionary with the link as key and the date as value
	return bookmarked
	
	# exit the program
	sys.exit()

#print(get_bookmarks())

#####################################
#  MAIN PROGRAM
#####################################
def delete():
	

	
	# Select the articles for deleting, they are as links in delete_list
	delete_list = list()
	fecha = datetime.datetime.now()
	fecha2 = fecha - datetime.timedelta(hours = 720 )
	bookmarks = get_bookmarks()
	artdate = get_articles()
	for item in artdate:
		if item in bookmarks:
			continue
		else:
			if artdate[item] < fecha2:
				delete_list.append(item)
	
	# open a database connection
	# be sure to change the host IP address, username, password and database name to match your own
	connection = None
	cursor = None
	try:
		connection = MySQLdb.connect (host = "frmc.mmb.pcb.ub.es", user = "dbw13", passwd = "dbw2016", db = "DBW13")
	except:
		sys.stderr.write("El programa no ha entrado en mysql \n")
	# prepare a cursor object using cursor() method
	cursor = connection.cursor ()

	# execute the SQL query using execute() method for each of the elements in the delete_list
	for hatti in delete_list:
		cursor.execute ("DELETE FROM search_news_article WHERE link ='%s';" % (hatti))

		# close the cursor object
	cursor.close ()

	# close the connection
	connection.close ()

	return delete_list


while True:
	sys.stdout = open("aitor.log", "a")
	for element in delete():
		sys.stdout.write(element + "\n")
	sys.stdout.close()
	time.sleep(7190)

