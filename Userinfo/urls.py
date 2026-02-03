# from django.urls import path
# from .views import ProfileView,profile_page
# urlpatterns=[
#     path('profile/',ProfileView.as_view()),
#     path("api/profile/", ProfileView.as_view(), name="api_profile"),
#     path("profile/", profile_page, name="profile_page"),
    
# ]

from django.urls import path
from .views import ProfileView, profile_page

urlpatterns = [
    #  HTML Profile Page
    path("profile/", profile_page, name="profile_page"),

    # DRF API Profile
    path("api", ProfileView.as_view(), name="api_profile"),
]
