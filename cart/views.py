from django.shortcuts import redirect, render
from signuplogin.models import Product

def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)

    cart[pid] = cart.get(pid, 0) + 1
    request.session["cart"] = cart

    return redirect("view_cart")


def view_cart(request):
    cart = request.session.get("cart", {})

    items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        subtotal = product.price * qty
        total += subtotal

        items.append({
            "product": product,
            "qty": qty,
            "subtotal": subtotal
        })

    return render(request, "cart.html", {"items": items, "total": total})


def remove_cart(request, product_id):
    cart = request.session.get("cart", {})
    pid = str(product_id)

    if pid in cart:
        del cart[pid]

    request.session["cart"] = cart
    return redirect("view_cart")

import uuid
from django.contrib.auth.decorators import login_required
from Userinfo.models import Order, OrderItem

from signuplogin.models import Product


@login_required
def checkout(request):
    cart = request.session.get("cart", {})

    if not cart:
        return redirect("view_cart")

    total = 0

    #  create new order
    order = Order.objects.create(
        user=request.user,
        order_id=str(uuid.uuid4())[:10],
        status="PLACED",
        total_amount=0,
        discount_amount=0
    )

    #  add items into order
    for pid, qty in cart.items():
        product = Product.objects.get(id=pid)
        subtotal = product.price * qty
        total += subtotal

        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            unit_price=product.price
        )

    #  update order total
    order.total_amount = total
    order.save()

    #  clear cart
    request.session["cart"] = {}

    return redirect("/userinfo/orders/")
