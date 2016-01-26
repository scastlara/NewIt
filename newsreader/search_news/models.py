from django.db import models

'''
Here we need to define our Database models
We should do it here beacause we will be able to use
django internal functions and the admin site.
'''

# TABLE FOR CATEGORIES
class Category(models.Model):
    category     = models.CharField(max_length=10, primary_key=True)
    synonyms     = models.TextField()
    num_articles = models.IntegerField()
    num_queries  = models.IntegerField()


# TABLES FOR ARTICLES
class Articles(models.Model):
    identifier  = models.IntegerField(primary_key=True)
    pubdate     = models.DateTimeField()
    title       = models.TextField()
    language    = models.CharField(max_length=3)
    content     = models.TextField()
    category    = models.CharField(max_length=10)
    #     "Category",
    #     on_delete = models.CASCADE,
    #     db_column='category'
    # )
    link       = models.URLField()
    source     = models.CharField(max_length=10)
    bookmarked = models.BooleanField()
