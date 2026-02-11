import random
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import redirect,render
from django.core.mail import send_mail
from django.contrib.auth.hashers import  make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PasswordResetOTP
from django.contrib.auth import authenticate, login
from .models import Category,Product
from rest_framework.permissions import  AllowAny
from .models import Category
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .models import Address
from django.contrib.auth import logout
from django.db.models import Count
from cart.models import CartItem, Wishlist
from django.db import IntegrityError
from cart.services import count
from django.db.models import Avg
from .models import Product, Review

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    VerifyOtpSerializer,
    ResetPasswordSerializer
)
class SignupView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        serializer = SignupSerializer(data=request.POST)

        if serializer.is_valid():
            try:
                user = serializer.save()
                login(request, user)
                return redirect("dashboard")

            except IntegrityError:
                # THIS STOPS THE CRASH
                return render(
                    request,
                    "signup.html",
                    {
                        "error": {
                            "username": ["Username already exists"]
                        },
                        "data": request.POST
                    }
                )

        return render(
            request,
            "signup.html",
            {
                "error": serializer.errors,
                "data": request.POST
            }
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        serializer = LoginSerializer(data=request.POST)

        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )

            if user:
                login(request, user)
                return redirect("splash")

            #  INVALID LOGIN MESSAGE
            return render(
                request,
                "login.html",
                {"error": "Invalid username or password"}
            )

        return render(
            request,
            "login.html",
            {"error": "Invalid input"}
        )


class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            
            email = serializer.validated_data["email"]

            user = user.objects.filter(email=email).first()
            if not user:
                return Response({"msg": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

            otp = str(random.randint(100000, 999999))

            # optional: delete old otps
            PasswordResetOTP.objects.filter(user=user).delete()

            PasswordResetOTP.objects.create(user=user, otp=otp)

            send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP is: {otp}",
                from_email=None,
                recipient_list=[email],
                fail_silently=False
            )

            return Response({"msg": "OTP sent to your email"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  Verify OTP Only
class VerifyOtpView(APIView):
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]

            user = user.objects.filter(email=email).first()
            if not user:
                return Response({"msg": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).first()
            if not otp_obj:
                return Response({"msg": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            #  expiry 10 min
            if timezone.now() - otp_obj.created_at > timedelta(minutes=10):
                return Response({"msg": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

            otp_obj.is_verified = True
            otp_obj.save()

            return Response({"msg": "OTP verified successfully "}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  Reset Password (Only if OTP verified)
class ResetPasswordView(APIView):
    
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            otp = serializer.validated_data["otp"]
            new_password = serializer.validated_data["new_password"]

            user = user.objects.filter(email=email).first()
            if not user:
                return Response({"msg": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

            otp_obj = PasswordResetOTP.objects.filter(user=user, otp=otp).first()
            if not otp_obj:
                return Response({"msg": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            # expiry check
            if timezone.now() - otp_obj.created_at > timedelta(minutes=10):
                return Response({"msg": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

            #  check verified
            if otp_obj.is_verified is False:
                return Response({"msg": "OTP not verified. Please verify OTP first."}, status=status.HTTP_400_BAD_REQUEST)

            #                    reset password
            user.password = make_password(new_password)
            user.save()

            #  delete OTP after successful reset
            otp_obj.delete()

            return Response({"msg": "Password reset successful "}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

def splash_page(request):
    return render(request, "splash.html")


def category_products(request, cat_id):
    category = Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category)
    return render(request, "category_products.html", {"category": category, "products": products})


def dashboard_page(request):
    categories = Category.objects.all()
    # TRENDING 
    trending_products = (
        Product.objects
        .annotate(cart_count=Count("cartitem"))
        .filter(cart_count__gt=0)
        .order_by("-cart_count")[:4]
    )
    if not trending_products.exists():
        trending_products = Product.objects.all()[:4]

    # RECOMMENDED (WISHLIST BASED) 
    recommended_products = Product.objects.none()

    if request.user.is_authenticated:
        wishlist_category_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list("product__category", flat=True)

        recommended_products = (
            Product.objects
            .filter(category__in=wishlist_category_ids)
            .exclude(wishlist__user=request.user)
            .distinct()[:4]
        )

    if not recommended_products.exists():
        recommended_products = Product.objects.all()[:4]

    #  OFFERS (LOW ENGAGEMENT PRODUCTS) 
    offer_products = (
        Product.objects
        .annotate(
            cart_count=Count("cartitem"),
            wishlist_count=Count("wishlist")
        )
        .filter(cart_count__lte=1, wishlist_count__lte=1)
        .order_by("?")[:4]
    )
      # -------- RECENTLY VIEWED --------
    recent_ids = request.session.get("recently_viewed", [])
    recently_viewed_products = Product.objects.filter(id__in=recent_ids)

    # Keep order same as session
    recently_viewed_products = sorted(
        recently_viewed_products,
        key=lambda x: recent_ids.index(x.id)
    )
    # --------------------------------

    return render(request, "dashboard.html", {
        "categories": categories,
        "trending_products": trending_products,
        "recommended_products": recommended_products,
        "offer_products": offer_products,
        "recently_viewed_products": recently_viewed_products,
    })


    
def settings_page(request):
    return render(request, "settings.html")


def set_language(request):
    if request.method == "POST":
        lang = request.POST.get("language")
        request.session["language"] = lang
    return redirect("settings")

def my_orders(request):
    return render(request, "my_orders.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def my_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "addresses.html", {"addresses": addresses})

@login_required
def add_address(request):
    if request.method == "POST":
        Address.objects.create(
            user=request.user,
            full_name=request.POST["full_name"],
            phone_number=request.POST["phone_number"],
            address_line=request.POST["address_line"],
            city=request.POST["city"],
            state=request.POST["state"],
            pincode=request.POST["pincode"],
            address_type=request.POST["address_type"],
        )
        return redirect("my_addresses")

    return render(request, "add_address.html")

@login_required
def delete_address(request, id):
    address = Address.objects.get(id=id, user=request.user)
    address.delete()
    return redirect("my_addresses")


@login_required
def edit_address(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)

    if request.method == "POST":
        address.full_name = request.POST["full_name"]
        address.phone_number = request.POST["phone_number"]
        address.address_line = request.POST["address_line"]
        address.city = request.POST["city"]
        address.state = request.POST["state"]
        address.pincode = request.POST["pincode"]
        address.address_type = request.POST["address_type"]
        address.save()

        return redirect("my_addresses")

    return render(request, "edit_address.html", {"address": address})



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




def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    #  SAVE REVIEW
    if request.method == "POST":
        if request.user.is_authenticated:

            rating = request.POST.get("rating")
            comment = request.POST.get("comment")

            if rating and comment:
                Review.objects.update_or_create(
                    product=product,
                    user=request.user,
                    defaults={
                        "rating": int(rating),
                        "comment": comment
                    }
                )

            return redirect("product_detail", product_id=product.id)

    # CALCULATE DATA 
    reviews = product.reviews.all()
    average_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0
    total_reviews = reviews.count()

    # RECENTLY VIEWED 
    viewed = request.session.get("recently_viewed", [])

    if product_id in viewed:
        viewed.remove(product_id)

    viewed.insert(0, product_id)
    request.session["recently_viewed"] = viewed[:4]
    request.session.modified = True

    return render(request, "product_detail.html", {
        "product": product,
        "reviews": reviews,
        "average_rating": average_rating,
        "total_reviews": total_reviews
    })
