from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from ECO import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ECO/', include('ECO.urls', namespace='ECO')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG is False:
    # from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    # urlpatterns += staticfiles_urlpatterns()  # django 1.8 以上不需要
    handler404 = views.page_not_found
    handler500 = views.page_error