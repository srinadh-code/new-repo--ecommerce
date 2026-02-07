
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from signuplogin.models import Product,Category
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
    # return redirect("dashboard")


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


from .models import Wishlist

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    messages.success(request, "Added to wishlist")
    # return redirect("dashboard")

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from signuplogin.models import Product

@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    )

    if wishlist_item.exists():
        wishlist_item.delete()   # ❤️ → 🤍
    else:
        Wishlist.objects.create(user=request.user, product=product)  # 🤍 → ❤️

    return redirect(request.META.get("HTTP_REFERER", "dashboard"))




@login_required
def wishlist_page(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, "wishlist.html", {"wishlist_items": wishlist_items})


@login_required
def remove_from_wishlist(request, product_id):
    Wishlist.objects.filter(
        user=request.user,
        product_id=product_id
    ).delete()

    messages.success(request, "Removed from wishlist")
    return redirect("wishlist")


@login_required
def wishlist_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    Wishlist.objects.filter(user=request.user, product=product).delete()

    messages.success(request, "Moved to cart")
    return redirect("view_cart")
from cart.models import Wishlist


def dashboard_page(request):
    categories = Category.objects.all()
    return render(request, "dashboard.html", {
        "categories": categories
    })

# def dashboard_page(request):
#     categories = Category.objects.all()
#     cart_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
#     wishlist_count = Wishlist.objects.filter(user=request.user).count() if request.user.is_authenticated else 0

#     return render(request, "dashboard.html", {
#         "categories": categories,
#         "cart_count": cart_count,
#         "wishlist_count": wishlist_count,
#     })
from cart.models import Wishlist

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    in_wishlist = False
    if request.user.is_authenticated:
        in_wishlist = Wishlist.objects.filter(
            user=request.user,
            product=product
        ).exists()

    return render(request, "product_detail.html", {
        "product": product,
        "in_wishlist": in_wishlist
    })
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from signuplogin.models import Product
# from .models import Wishlist, CartItem
# @login_required
# def add_to_wishlist(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     Wishlist.objects.get_or_create(user=request.user, product=product)
#     return redirect(request.META.get("HTTP_REFERER", "dashboard"))
# @login_required
# def remove_from_wishlist(request, product_id):
#     Wishlist.objects.filter(user=request.user, product_id=product_id).delete()
#     return redirect(request.META.get("HTTP_REFERER", "wishlist"))
# @login_required
# def wishlist_page(request):
#     wishlist_items = Wishlist.objects.filter(user=request.user)
#     return render(request, "wishlist.html", {"wishlist_items": wishlist_items})
# @login_required
# def wishlist_to_cart(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     cart_item, _ = CartItem.objects.get_or_create(
#         user=request.user,
#         product=product
#     )
#     cart_item.quantity += 1
#     cart_item.save()

#     Wishlist.objects.filter(user=request.user, product=product).delete()
#     return redirect("view_cart")
# from cart.models import Wishlist, CartItem

# def dashboard_page(request):
#     categories = Category.objects.all()
#     cart_count = CartItem.objects.filter(user=request.user).count() if request.user.is_authenticated else 0
#     wishlist_count = Wishlist.objects.filter(user=request.user).count() if request.user.is_authenticated else 0

#     return render(request, "dashboard.html", {
#         "categories": categories,
#         "cart_count": cart_count,
#         "wishlist_count": wishlist_count
#     })
from .models import Wishlist, CartItem

def cart_wishlist_counts(request):
    if request.user.is_authenticated:
        return {
            "cart_count": CartItem.objects.filter(user=request.user).count(),
            "wishlist_count": Wishlist.objects.filter(user=request.user).count(),
        }
    return {
        "cart_count": 0,
        "wishlist_count": 0,
    }
from cart.models import Wishlist

def category_products(request, cat_id):
    category = Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category)

    wishlist_ids = []
    if request.user.is_authenticated:
        wishlist_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list("product_id", flat=True)

    return render(request, "category_products.html", {
        "category": category,
        "products": products,
        "wishlist_ids": wishlist_ids
    })
from django.db.models import Q
from signuplogin.models import Product, Category

def search_view(request):
    query = request.GET.get("q", "")

    products = Product.objects.filter(
        Q(name__icontains=query)
    )

    categories = Category.objects.filter(
        Q(name__icontains=query)
    )

    return render(request, "search_results.html", {
        "query": query,
        "products": products,
        "categories": categories
    })
