from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CartItem, Order, OrderItem,Wishlist

admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)