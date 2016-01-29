from django.conf.urls import include, url
from . import views
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.index_view),
        # Registration URLs
    url(r'^accounts/register/$', views.register, name='register'),
    url(r'^accounts/register/complete/$', views.registration_complete),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', lambda request: logout_then_login(request, "/"), name='logout'),
    url(r'^accounts/loggedin/$', views.loggedin),
]
