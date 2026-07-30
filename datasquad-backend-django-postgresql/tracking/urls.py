from django.urls import path
from . import views

urlpatterns = [
    path("track/", views.track_pageview, name="track_pageview"),
]
