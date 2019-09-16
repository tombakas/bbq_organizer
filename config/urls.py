from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from bbq_organizer.views import view_404

urlpatterns = [
    path("", include("bbq_organizer.urls")),

    # Admin
    path("admin/", admin.site.urls),

    # Authentication handling
    path("accounts/", include("django.contrib.auth.urls")),
]

handler404 = view_404
