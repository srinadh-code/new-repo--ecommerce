# from.views import signupview,loginview,forgotpasswordview,resetpasswordview
# from django.urls import path
# urlpatterns = [    
#     path("",signupview.as_view(),name="signup"),
#     path("login/",loginview.as_view(),name="login"),
#     path("forgot/",forgotpasswordview.as_view(),name="forgot"),
#     path("reset/",resetpasswordview.as_view(),name="reset"),
    
# ]


from django.urls import path
from .views import (
    SignupView,
    LoginView,
    ForgotPasswordView,
    VerifyOtpView,
    ResetPasswordView,
    splash_page,
    
    dashboard_page, category_products

    
)

urlpatterns = [

    path("", SignupView.as_view()),
    path("login/", LoginView.as_view()),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("splash/", splash_page, name="splash"),
    path("dashboard/", dashboard_page, name="dashboard"),
    path("category/<int:cat_id>/", category_products, name="category_products"),
    

]
