# bmh_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hospital.urls")),   # all hospital app URLs are rooted here
    path("pharmacy/", include("pharmacy.urls")),
    path("accounts/", include("accounts.urls")),
]

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)