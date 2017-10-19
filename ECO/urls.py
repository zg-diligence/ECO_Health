from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^home/$', views.Home, name='home'),
    url(r'^profile/about_me/$', views.UserInfo, name='about_me'),
    url(r'^profile/user_conditions/$', views.UserConditions, name="user_disease"),
    url(r'^profile/user_conditions/symptoms/$', views.UserSymptoms, name="user_symptoms"),
    url(r'^profile/user_conditions/treatments/$', views.UserTreatments, name="user_treatments"),
    url(r'^conditions/$', views.DiseIndex, name='disease_index'),
    url(r'^conditions/(?P<dise_id>\d+)/overview/$', views.DiseOverview, name='overview'),
    url(r'^conditions/(?P<dise_id>\d+)/symptoms/$', views.DiseSymptoms, name='symptoms'),
    url(r'^conditions/(?P<dise_id>\d+)/treatments/$', views.DiseTreatments, name='treatments'),
    url(r'^conditions/compare_treatments/$', views.DiseCompareTreatments, name='compare_treatments'),
    url(r'^conditions/evaluate_treatments/$', views.DiseEvaluateTreatments, name='evaluate_treatments'),
    url(r'^interact/$', views.InteractIndex, name='interact_index'),
    url(r'^interact/patients/$', views.InteractPatients, name='patients'),
    url(r'^interact/user_say/$', views.InteractUserSay, name='user_say'),
    url(r'^interact/advanced_study/$', views.InteractAdvancedStudy, name='advance_study'),
]