from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import login
from django.contrib.auth.views import password_change, password_change_done
urlpatterns = [
    url(r'^$', views.index_view, name='index_view'),
        # Registration URLs
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/complete/$', views.registration_complete),
    url(r'^accounts/login/$', login, name ='login'),
    url(r'^accounts/logout/$', lambda request: logout_then_login(request, "/"), name='logout'),
    url(r'^accounts/loggedin/$', views.loggedin),
    url(r'^accounts/change_password/$', password_change, name="change_password"),
    url(r'^accounts/change_password_done/$', password_change_done, name="password_change_done"),
    url(r'^subscribed$', views.subscribed, name='subscribed'),
    url(r'^unsubscribed$', views.unsubscribed, name='unsubscribed'),
    url(r'^news/(?P<diario>.+)/$', views.index_view, name = 'news'),
    url(r'^accounts/search_subscritions/$', views.user_subscriptions, name="user_subscriptions"),
    url(r'^accounts/feed_subscriptions/$',  views.feed_subscriptions, name="feed_subscriptions"),
    url(r'^accounts/bookmarks/$', views.user_bookmarks, name ="user_bookmarks"),
    url(r'^accounts/booked/$', views.user_booked, name ="user_booked"),
]
