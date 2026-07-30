from django.urls import path

from . import views

urlpatterns = [
    path("actus/", views.actus_list, name="actus_list"),
    path("equipe/", views.equipe_list, name="equipe_list"),
]
