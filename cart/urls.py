from django.urls import path
from . import views
from .views import search_view, wishlist_page,add_to_wishlist,remove_from_wishlist,wishlist_to_cart, toggle_wishlist
urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("view/", views.view_cart, name="view_cart"),
    path("remove/<int:item_id>/", views.remove_cart, name="remove_cart"),
    path("decrease/<int:item_id>/", views.decrease_qty, name="decrease_qty"),
    #  Cart Place Order
    path("place-order/", views.place_order, name="place_order"),
    path("my-orders/", views.my_orders, name="my_orders"),

    #  Buy 
    path("search/", search_view, name="search"),
    
    
    # path("product/<int:product_id>/", views.product_detail, name="product_detail"),
    path("buy/<int:product_id>/", views.place_order_single, name="place_order_single"),
    path("order-success/<int:order_id>/", views.order_success, name="order_success"),
    path("delete-order/<int:order_id>/", views.delete_order, name="delete_order"),
    path("wishlist/", wishlist_page, name="wishlist"),
    path("wishlist/add/<int:product_id>/", add_to_wishlist, name="add_to_wishlist"),
    path("wishlist/remove/<int:product_id>/", remove_from_wishlist, name="remove_from_wishlist"),
    path("wishlist/move-to-cart/<int:product_id>/", wishlist_to_cart, name="wishlist_to_cart"),
    path("wishlist/toggle/<int:product_id>/", toggle_wishlist, name="toggle_wishlist"),
    path("subcategory/<int:sub_id>/", views.subcategory_products, name="subcategory_products")

]
