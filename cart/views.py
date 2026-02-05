
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from signuplogin.models import Product
from .models import CartItem, Order, OrderItem
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return redirect("view_cart")
@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)

    total = 0
    for item in cart_items:
        total += item.subtotal()

    return render(request, "cart.html", {
        "cart_items": cart_items,
        "total": total
    })
@login_required
def remove_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("view_cart")
@login_required
def decrease_qty(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("view_cart")
#  for Placing order 
@login_required
def place_order(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("view_cart")

    # for Create order
    order = Order.objects.create(user=request.user)

    total = 0
    for item in cart_items:
        total += item.subtotal()

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            unit_price=item.product.price
        )

    order.total_amount = total
    order.save()

    #  Clear cart
    cart_items.delete()

    messages.success(request, " Order placed successfully!")
    return redirect("my_orders")


#  MY ORDERS PAGE 
@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "my_orders.html", {"orders": orders})

#  Product Detail Page 
@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})

#  Place Order from product detail page
@login_required
def place_order_single(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    #  Create Order
    order = Order.objects.create(user=request.user)

    #  Create OrderItem
    OrderItem.objects.create(
        order=order,
        product=product,
        quantity=1,
        unit_price=product.price
    )
    order.total_amount = product.price
    order.save()
    return redirect("order_success", order_id=order.id)

#  Order Success Page
@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_success.html", {"order": order})

@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.delete()
    return redirect("my_orders")