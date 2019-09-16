from django.urls import path
from bbq_organizer import views

from django.urls import re_path


urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("create_event/", views.create_event, name="create_event"),
    path("events/admin/<str:slug>", views.admin_event, name="admin_event"),
    path("events/invite/<str:slug>", views.invite_event, name="invite_event"),
    path("events/invite/register/<str:slug>", views.register_event, name="register_event"),
    path("events/list", views.events_list, name="events_list"),
    path("thank_you", views.thank_you, name="thank_you"),
]
