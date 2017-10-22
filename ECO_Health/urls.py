from django.conf.urls import url, include
from django.contrib import admin
from ECO import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ECO/', include('ECO.urls', namespace='ECO')),
    #url(r'^index/', views.Index, name='index'),
    #url(r'^login_with_username/', views.LoginWithUsername, name='login_with_username'),
    #url(r'^login_with_email/', views.LoginWithEmail, name='login_with_email'),
    #url(r'^register/', views.Register, name='register'),
]