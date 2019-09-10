from django.urls import path
from django.contrib import admin
from django.conf.urls import include

from bbq_organizer import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.home)
]
