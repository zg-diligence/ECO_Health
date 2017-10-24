from .views import *
from django.conf.urls import url, include

disease_pattern = [
    url(r'^$', disease_index, name='disease_index'),
    url(r'^(?P<disease_id>[0-9]+)/$', disease_detail, name='disease_detail'),
]

symptom_pattern = [
    url(r'^$', symptom_index, name='symptom_index'),
]

treatment_pattern = [
    url(r'^$', treatment_index, name='treatment_index'),
]

person_pattern = [
    url(r'^$', person_index, name='person_index'),
]

social_pattern = [
    url(r'^$', social_index, name='social_index'),
]

app_name = 'ECO'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^home$', home, name='home'),
    url(r'^user_login$', user_login, name='user_login'),
    url(r'^disease_index/', include(disease_pattern)),
    url(r'^treatment_index/', include(treatment_pattern)),
    url(r'^symptom_index/', include(symptom_pattern)),
    url(r'^person_index/', include(person_pattern)),
    url(r'^social_index/', include(social_pattern)),
]