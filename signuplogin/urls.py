from django.urls import path
from .views import settings_page
from .views import set_language, my_orders, logout_view
from .views import (
    SignupView,
    LoginView,
    ForgotPasswordView,
    VerifyOtpView,
    ResetPasswordView,
    splash_page,
    dashboard_page,
    category_products,
    product_detail
)

urlpatterns = [

    path("", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(),name="login"),
    path("forgot-password/", ForgotPasswordView.as_view()),
    path("verify-otp/", VerifyOtpView.as_view()),
    path("reset-password/", ResetPasswordView.as_view()),
    path("splash/", splash_page, name="splash"),
    path("dashboard/", dashboard_page, name="dashboard"),
    
    path("settings/", settings_page, name="settings"),
    path("set-language/", set_language, name="set_language"),
    path("my-orders/", my_orders, name="my_orders"),
    path("logout/", logout_view, name="logout"),
    
    path("category/<int:cat_id>/", category_products, name="category_products"),
    path("product/<int:product_id>/", product_detail, name="product_detail"),   

]
