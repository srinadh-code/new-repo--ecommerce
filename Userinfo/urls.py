from django.urls import path
from .views import ProfileView,OrderlistView,ResetPasswordView
urlpatterns=[
    path('profile/',ProfileView.as_view()),
    path('orders/',OrderlistView.as_view()),
    path('resetpassword/',ResetPasswordView.as_view()),

]