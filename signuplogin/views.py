
# from .serializers import signupserializers
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .serializers import loginserializers
# from .models import signup
# from django.core.mail import send_mail

# class signupview(APIView):
#     def post(self,request):
#         serializer=signupserializers(data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {"message ": "signup successful" ,"data":serializer.data    },
#                 status=status.HTTP_201_CREATED
#             )
        
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

# class loginview(APIView):
#     def post(self,request):
#         serializer=loginserializers(data=request.data)
        
        
#         if serializer.is_valid():
#             username=serializer.validated_data["username"]
#             password=serializer.validated_data["password"]
#             user=signup.objects.filter(username=username,password=password).first()
#             if user:
#                 return Response({"msg":"login succesful"},status=200)
#             return Response({"msg":"inavlid usernam or password"},status=401)
    
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
# import random
# # from datetime import timedelta
# from django.utils import timezone
# from django.core.mail import send_mail

# from .serializers import forgotpassword

# class forgotpasswordview(APIView):
#     def post(self,request):
#         serializer=forgotpassword(data=request.data)
        

#         if serializer.is_valid():
#             email=serializer.validated_data["email"]
            
#             user=signup.objects.filter(email=email).first()
#             if not user:
#                 return Response({"msg":"email not found"},status=status.HTTP_404_NOT_FOUND)
            
#             otp=str(random.randint(100000,999999))
#             user.reset_otp=otp
#             user.otp_created_at=timezone.now()

#             # if timezone.now() - user.otp_created_at > timedelta (minutes=10):
#             #     return Response({"message": "OTP expired"},status=status.HTTP_400_BAD_REQUEST)
#             user.save()
             
#             send_mail(
#                 subject="password reset otp",
#                 message=f"your otp is{otp}",
#                 from_email=None,
#                 recipient_list=[email],
#                 fail_silently=True
#             )
            
            
#             return Response({"msg":"otp sent to email"},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
# from.serializers import resetpassword
# class resetpasswordview(APIView):
#     def post(self,request):
#         serializer=resetpassword(data=request.data)
        
#         if serializer.is_valid():
#             email=serializer.validated_data["email"]
#             otp=serializer.validated_data["otp"]
#             new_password=serializer.validated_data["new_password"]
            
            
#             user=signup.objects.filter(email=email,reset_otp=otp).first()
            
            
#             if not user:
#                 return Response({"msessage":"invalid otp"},status=status.HTTP_400_BAD_REQUEST)
#             user.password=new_password
#             user.reset_otp=None
#             user.otp_created_at=None
#             user.save()
#             return Response({"msg":"password rest secussful"},status=status.HTTP_200_OK)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
import random
from datetime import timedelta
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Signup, PasswordResetOTP
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    ForgotPasswordSerializer,
    VerifyOtpSerializer,
    ResetPasswordSerializer
)


# ✅ Signup
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Signup successful"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#  Login
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            user = Signup.objects.filter(username=username).first()

            if user and check_password(password, user.password):
                return redirect("splash")
                # return Response({"msg": "Login successful"}, status=status.HTTP_200_OK)
                

            return Response({"msg": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)

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

            #  expiry check
            if timezone.now() - otp_obj.created_at > timedelta(minutes=10):
                return Response({"msg": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)

            #  check verified
            if otp_obj.is_verified is False:
                return Response({"msg": "OTP not verified. Please verify OTP first."}, status=status.HTTP_400_BAD_REQUEST)

            #  reset password
            user.password = make_password(new_password)
            user.save()

            #  delete OTP after successful reset
            otp_obj.delete()

            return Response({"msg": "Password reset successful "}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# from django.shortcuts import render
# from .models import Banner

# def splash_page(request):
#     banner = Banner.objects.filter(is_active=True).last()   # latest active banner
#     return render(request, "splash.html", {"banner": banner})

from django.shortcuts import render, redirect

def splash_page(request):
    return render(request, "splash.html")

from django.shortcuts import render

def dashboard_page(request):
    return render(request, "dashboard.html")

from django.shortcuts import render
from .models import Category,Product

def dashboard_page(request):
    categories = Category.objects.all()
    return render(request, "dashboard.html", {"categories": categories})

def category_products(request, cat_id):
    category = Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category)
    return render(request, "category_products.html", {"category": category, "products": products})
