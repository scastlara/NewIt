from django.db import models

# Here we need to define our Database models
# We should do it here beacause we will be able to use
# django internal functions and the admin site.
# Create your models here.


class Notisiario(models.Model):
    ID             = models.IntegerField(primary_key=True, max_length=20)
    DATE           = models.DateTimeField()
    CATEGO         = models.FileField(max_length=50)
    TITLE          = models.FileField(max_length=255)
    created_date   = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
