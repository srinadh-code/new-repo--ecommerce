from django.urls import path
from .views import ProfileView, OrderListView, ChangePasswordView, LogoutView

urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("orders/", OrderListView.as_view(), name="orders"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
