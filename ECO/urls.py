from .views import *
from django.conf.urls import url

app_name = 'ECO'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^home$', home, name='home'),
    url(r'^user_login$', user_login, name='user_login'),
    url(r'^disease_index/$',disease_index, name='disease_index'),
    url(r'^disease/(?P<disease_id>[0-9]+)/$', disease_detail, name='disease_detail'),
]