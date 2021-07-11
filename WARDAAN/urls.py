from django.contrib import admin
from django.urls import path, include
from home import urls
from doctor import urls
from patient import urls
from blogs import urls
from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("doctor/", include("doctor.urls")),
    path("patient/", include("patient.urls")),
    path("blogs/", include("blogs.urls")),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
