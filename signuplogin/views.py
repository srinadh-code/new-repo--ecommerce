import random
from datetime import timedelta
from django.shortcuts import redirect,render
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Signup, PasswordResetOTP
from django.shortcuts import render

from django.shortcuts import render
from .models import Category,Product
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    VerifyOtpSerializer,
    ResetPasswordSerializer
)
from rest_framework.permissions import  AllowAny

#  Signup
class SignupView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = SignupSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return redirect("dashboard") 
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 def post(self, request):
        #  Check incoming request data
        print("DEBUG: Signup request received")
        print("DEBUG: Request data:", request.data)

        serializer = SignupSerializer(data=request.data)

        # Check serializer validation
        if serializer.is_valid():
            print("DEBUG: Serializer is valid")
            print("DEBUG: Validated data:", serializer.validated_data)

            user = serializer.save()
            print("DEBUG: User saved successfully")
            print("DEBUG: User ID:", user.id)
            print("DEBUG: Username:", user.username)
            # return Response({"username":user.username,"email":user.email})
            

            return redirect("dashboard")

        #  If validation fails
        print("DEBUG: Serializer validation failed")
        print("DEBUG: Errors:", serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  Login
class LoginView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = Signup.objects.filter(username=username).first()
            if user and check_password(password, user.password):
                # return Response({"msg": "login sucessful","username":username,"password":password})
                return redirect("splash")
               

            # return Response({"msg": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  Forgot Password (Send OTP)
class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            
            email = serializer.validated_data["email"]

            user = Signup.objects.filter(email=email).first()
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

            user = Signup.objects.filter(email=email).first()
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

            user = Signup.objects.filter(email=email).first()
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

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, "product_detail.html", {"product": product})
from django.shortcuts import render, get_object_or_404
from .models import Product

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