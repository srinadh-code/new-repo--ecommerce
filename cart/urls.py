from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("view/", views.view_cart, name="view_cart"),
    path("remove/<int:item_id>/", views.remove_cart, name="remove_cart"),
    path("decrease/<int:item_id>/", views.decrease_qty, name="decrease_qty"),
    #  Cart Place Order
    path("place-order/", views.place_order, name="place_order"),
    path("my-orders/", views.my_orders, name="my_orders"),

    #  Buy 
    path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("buy/<int:product_id>/", views.place_order_single, name="place_order_single"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path("delete-order/<int:order_id>/", views.delete_order, name="delete_order"),
    
]
