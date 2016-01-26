from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.index_view),
    url(r'^register/$', views.register_view),
]
