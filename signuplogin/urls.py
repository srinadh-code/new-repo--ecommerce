from.views import signupview,loginview,forgotpasswordview,resetpasswordview
from django.urls import path
urlpatterns = [    
    path("",signupview.as_view(),name="signup"),
    path("login/",loginview.as_view(),name="login"),
    path("forgot/",forgotpasswordview.as_view(),name="forgot"),
    path("reset/",resetpasswordview.as_view(),name="reset"),
    
]
