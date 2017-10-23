from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from ECO import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ECO/', include('ECO.urls', namespace='ECO')),
]

if settings.DEBUG is False:
    urlpatterns += staticfiles_urlpatterns()
    handler404 = views.page_not_found
    handler500 = views.page_error