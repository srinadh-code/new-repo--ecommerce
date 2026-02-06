import random
from datetime import timedelta
from django.shortcuts import redirect,render
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.hashers import  make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PasswordResetOTP
from django.contrib.auth import authenticate, login
from .models import Category,Product
from rest_framework.permissions import  AllowAny
from .models import Category
from django.shortcuts import render, get_object_or_404
from .models import Product
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    VerifyOtpSerializer,
    ResetPasswordSerializer
)

class SignupView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user) 
            return redirect("dashboard")
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"]
            )

            if user:
                login(request, user)
                return redirect("splash")

            return Response(
                {"msg": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
from .models import Category

def dashboard_page(request):
    categories = Category.objects.all()
    return render(request, "dashboard.html", {"categories": categories})
from django.shortcuts import render, get_object_or_404
from .models import Product

# def product_detail(request, id):
#     product = get_object_or_404(Product, id=id)
#     return render(request, "product_detail.html", {"product": product})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "product_detail.html", {"product": product})

def settings_page(request):
    return render(request, "settings.html")
from django.shortcuts import redirect, render
from django.contrib.auth import logout

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



from django.contrib.auth.decorators import login_required
from .models import Address

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
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Address

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
