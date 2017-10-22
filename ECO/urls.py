from .views import *
from django.conf.urls import url

urlpatterns = [
    url(r'^$',index, name='index'),
    url(r'^disease_index/$',disease_index,name='disease_index'),
    url(r'^(?P<disease_id>[0-9]+)/$',disease_detail, name='disease_detail'),
]