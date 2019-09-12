from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from bbq_organizer import views

urlpatterns = [
    path("", views.home, name="home"),
    path("admin/", admin.site.urls),

    # Authentication handling
    path("signup/", views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
]
