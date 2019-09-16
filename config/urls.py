from django.urls import path
from django.contrib import admin
from django.conf.urls import include

urlpatterns = [
    path("", include("bbq_organizer.urls")),

    # Admin
    path("admin/", admin.site.urls),

    # Authentication handling
    path("accounts/", include("django.contrib.auth.urls")),
]
