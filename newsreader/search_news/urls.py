from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index_view, name='index_view'),
        # Registration URLs
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/complete/$', views.registration_complete),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', lambda request: logout_then_login(request, "/"), name='logout'),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^subscribed$', views.subscribed, name='subscribed'),
    url(r'^news/(?P<diario>.+)/$', views.index_view),
    url(r'^accounts/search_subscritions/$', views.user_subscriptions, name="user_subscriptions"),
    url(r'^accounts/feed_subscriptions/$',  views.feed_subscriptions, name="feed_subscriptions"),

]
