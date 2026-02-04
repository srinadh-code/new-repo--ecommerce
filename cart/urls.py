from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("view/", views.view_cart, name="view_cart"),
    path("remove/<int:item_id>/", views.remove_cart, name="remove_cart"),
    path("decrease/<int:item_id>/", views.decrease_qty, name="decrease_qty"),
]
