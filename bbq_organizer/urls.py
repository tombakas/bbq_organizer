from django.urls import path
from bbq_organizer import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup, name="signup"),
    path("create_event/", views.create_event, name="create_event"),
    path("events/admin/<str:slug>", views.admin_event, name="admin_event"),
    path("events/list", views.events_list, name="events_list")
]
