from django.urls import path
from .views import RegisterView, GoogleSignInView, UserProfileView

urlpatterns = [
    path("register/",RegisterView.as_view(),name="register"),
    path("google/",GoogleSignInView.as_view(),name="google-signin"),
    path("profile/",UserProfileView.as_view(),name="user-profile"),

]