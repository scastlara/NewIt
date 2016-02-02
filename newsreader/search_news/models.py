from django.db import models


'''
Here we need to define our Database models
We should do it here beacause we will be able to use
django internal functions and the admin site.
'''


class Category(models.Model):
    category = models.CharField(max_length=20, primary_key=True)


class Article(models.Model):
    link        = models.URLField(primary_key=True)
    pubdate     = models.DateTimeField()
    title       = models.TextField()
    language    = models.CharField(max_length=3)
    content     = models.TextField()
    category    = models.CharField(max_length=20)
    source     = models.CharField(max_length=20)
    bookmarked = models.BooleanField()


class Feed(models.Model):
    link     = models.URLField(primary_key=True)
    name     = models.CharField(max_length=20) # Articles -> Sources
    category = models.CharField(max_length=20) # Category -> category
    language = models.CharField(max_length=3,default='ESP')


class Source(models.Model):
    name     = models.CharField(max_length=20, primary_key=True)
    homepage = models.URLField()
    logo     = models.CharField(max_length=20)


class Search_Subscription(models.Model):
    username = models.CharField(max_length=30) # auth_user -> username
    keyword  = models.CharField(max_length=100)
    category = models.CharField(max_length=20) # Category -> category


class Source_Subscription(models.Model):
    username = models.CharField(max_length=30) # auth_user -> username
    source   = models.CharField(max_length=20) # Sources -> name


class Bookmark(models.Model):
    username = models.CharField(max_length=30)
    article  = models.URLField(primary_key=False)
