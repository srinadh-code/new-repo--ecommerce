from django.urls import path
from .views import ProfileView,profile_page
urlpatterns=[
    path('profile/',ProfileView.as_view()),

    
]


