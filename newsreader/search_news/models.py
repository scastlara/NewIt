from django.db import models


'''
Here we need to define our Database models
We should do it here beacause we will be able to use
django internal functions and the admin site.
'''

# TABLE FOR CATEGORIES
class Category(models.Model):
    category     = models.CharField(max_length=10, primary_key=True)

# TABLES FOR ARTICLES
class Articles(models.Model):
    identifier  = models.IntegerField(primary_key=True)
    pubdate     = models.DateTimeField()
    title       = models.TextField()
    language    = models.CharField(max_length=3)
    content     = models.TextField()
    category    = models.CharField(max_length=10)
    link       = models.URLField()
    source     = models.CharField(max_length=10)
    bookmarked = models.BooleanField()

class Sources(models.Model):
    link     = models.URLField(primary_key=True)
    name     = models.CharField(max_length=10) # Articles -> Sources
    category = models.CharField(max_length=10) # Category -> category

class Search_Subscriptions(models.Model):
    username = models.CharField(max_length=30) # auth_user -> username
    keyword  = models.CharField(max_length=100)
    category = models.CharField(max_length=10) # Category -> category

class Source_Subscriptions(models.Model):
    username = models.CharField(max_length=30) # auth_user -> username
    source   = models.CharField(max_length=10) # Sources -> name
