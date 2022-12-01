from django.urls import path

from machine import views

urlpatterns = [
    path("", views.APIRoot.as_view(), name="home")
]
