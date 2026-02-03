from django.shortcuts import redirect, render
from signuplogin.models import Product
from django.shortcuts import redirect, render
from signuplogin.models import Product


def add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session["cart"] = cart

    return redirect("cart")


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

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


def remove_cart(request, product_id):

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session["cart"] = cart

    return redirect("cart")
def add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session["cart"] = cart

    return redirect("view_cart")



def add_to_cart(request, product_id):

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

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

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


def remove_cart(request, product_id):

    cart = request.session.get("cart", {})

    if str(product_id) in cart:
        del cart[str(product_id)]

    request.session["cart"] = cart

    return redirect("view_cart")
