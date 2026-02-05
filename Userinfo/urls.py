from django.urls import path
from .views import ProfileView, profile_page, delete_profile

urlpatterns = [
    path("profile-api/", ProfileView.as_view(), name="profile_api"),   #  JSON API
    path("profile-page/", profile_page, name="profile_page"), #  HTML page

    path("delete-profile/", delete_profile, name="delete_profile"),#  HTML page
]

