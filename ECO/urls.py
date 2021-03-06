from .views import *
from django.conf.urls import url, include

disease_pattern = [
    url(r'^$', disease_index, name='disease_index'),
    url(r'^(?P<disease_id>[0-9]+)/$', disease_detail, name='disease_detail'),
]

symptom_pattern = [
    url(r'^$', symptom_index, name='symptom_index'),
    url(r'^(?P<symptom_id>[0-9]+)/$', symptom_detail, name='symptom_detail'),
]

treatment_pattern = [
    url(r'^$', treatment_index, name='treatment_index'),
    url(r'^(?P<treatment_id>[0-9]+)/$', treatment_detail, name='treatment_detail'),
]

person_pattern = [
    url(r'^$',person_disease,name='person_index'),
    url(r'^person_disease/$',person_disease,name='person_disease'),
    url(r'^person_symptom/$',person_symptom,name='person_symptom'),
    url(r'^person_treatment/$',person_treatment,name='person_treatment'),
    url(r'^person_info/$',person_info,name='person_info'),
    url(r'^person_update/$',person_update,name='person_update'),
    url(r'^person_diagram/$',person_diagram,name='person_diagram'),
]

social_pattern = [
    url(r'^$',social_friendstate, name='social_index'),
    url(r'social_friendstate/$',social_friendstate,name='social_friendstate'),
    url(r'social_friendlist/$',social_friendlist,name='social_friendlist'),
    url(r'social_sendstate/$',social_sendstate,name='social_sendstate'),
    url(r'social_newfriend/$',social_newfriend,name='social_newfriend'),
    url(r'social_heart/$',social_heart,name='social_heart'),
]

app_name = 'ECO'
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^user_login$', user_login, name='user_login'),
    url(r'^user_register$', user_register, name='user_register'),
    url(r'^user_logout$', user_logout, name='user_logout'),
    url(r'^disease/', include(disease_pattern)),
    url(r'^treatment/', include(treatment_pattern)),
    url(r'^symptom/', include(symptom_pattern)),
    url(r'^person/', include(person_pattern)),
    url(r'^social/', include(social_pattern)),
]