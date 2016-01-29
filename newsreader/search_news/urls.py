from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import logout_then_login

urlpatterns = [
    url(r'^$', views.index_view),
        # Registration URLs
    url(r'^accounts/register/$', 'search_news.views.register', name='register'),
    url(r'^accounts/register/complete/$', 'search_news.views.registration_complete',
     name='registration_complete'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^accounts/logout/$', lambda request: logout_then_login(request, "/"), name='logout'),
    url(r'^accounts/loggedin/$', 'search_news.views.loggedin', name='loggedin'),
]
