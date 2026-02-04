from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from signuplogin.models import Product
from .models import CartItem


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
