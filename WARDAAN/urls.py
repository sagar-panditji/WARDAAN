from django.contrib import admin
from django.urls import path, include
from home import urls
from doctor import urls
from patient import urls
from blogs import urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("home/", include("home.urls")),
    path("doctor/", include("doctor.urls")),
    path("patient/", include("patient.urls")),
    path("blogs/", include("blogs.urls")),
]
