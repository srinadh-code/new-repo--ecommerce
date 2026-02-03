from django.urls import path
from .views import (
    SignupView,
    LoginView,
    ForgotPasswordView,
    VerifyOtpView,
    ResetPasswordView,
    splash_page,
    dashboard_page,
    category_products,
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
