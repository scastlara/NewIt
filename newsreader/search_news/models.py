from django.db import models

'''
Here we need to define our Database models
We should do it here beacause we will be able to use
django internal functions and the admin site.
'''


# MAIN TABLE WITH EVERYTHING
class Notisiario(models.Model):
    identifier = models.IntegerField(primary_key=True)
    pubdate    = models.DateField()
    category   = models.CharField(max_length=15)
    title      = models.TextField()
    language   = models.CharField(max_length=3)
    content    = models.TextField()
    link       = models.URLField()
    source     = models.CharField(max_length=10)
