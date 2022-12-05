from django.urls import path

from machine import views

urlpatterns = [
    path("", views.APIRoot.as_view(), name="home"),
    path("users", views.UserCreateView.as_view()),
    path("login", views.UserLoginView.as_view()),
    path("logout", views.LogoutView.as_view()),
    path("logout/all", views.LogoutAllView.as_view()),
]
