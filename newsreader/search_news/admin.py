from django.contrib import admin
from .models import Article, Category, Feed, Search_Subscription, Source_Subscription, Bookmark, Source

admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Feed)
admin.site.register(Search_Subscription)
admin.site.register(Source_Subscription)
admin.site.register(Bookmark)
admin.site.register(Source)
