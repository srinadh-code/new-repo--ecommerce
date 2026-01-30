
from .serializers import signupserializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import loginserializers
from .models import signup
from django.core.mail import send_mail

class signupview(APIView):
    def post(self,request):
        serializer=signupserializers(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message ": "signup successful" ,"data":serializer.data    },
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        

class loginview(APIView):
    def post(self,request):
        serializer=loginserializers(data=request.data)
        
        
        if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=signup.objects.filter(username=username,password=password).first()
            if user:
                return Response({"msg":"login succesful"},status=200)
            return Response({"msg":"inavlid usernam or password"},status=401)
    
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
import random
from django.utils import timezone
from django.core.mail import send_mail

from .serializers import forgotpassword

class forgotpasswordview(APIView):
    def post(self,request):
        serializer=forgotpassword(data=request.data)

        if serializer.is_valid():
            email=serializer.validated_data["email"]
            
            user=signup.objects.filter(email=email).first()
            if not user:
                return Response({"msg":"email not found"},status=status.HTTP_404_NOT_FOUND)
            
            otp=str(random.randint(100000,999999))
            user.reset_otp=otp
            user.otp_created_at=timezone.now()
            user.save()
            
            send_mail(
                subject="passwoed restet otp",
                message=f"your otp is{otp}",
                from_email=None,
                recipient_list=[email],
                fail_silently=True
            )
            
            return Response({"msg":"otp sent to email"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
    
from.serializers import resetpassword
class resetpasswordview(APIView):
    def post(self,request):
        serializer=resetpassword(data=request.data)
        
        if serializer.is_valid():
            email=serializer.validated_data["email"]
            otp=serializer.validated_data["otp"]
            new_password=serializer.validated_data["new_password"]
            
            
            user=signup.objects.filter(email=email,reset_otp=otp).first()
            
            
            if not user:
                return Response({"msessage":"invalid otp"},status=status.HTTP_400_BAD_REQUEST)
            user.password=new_password
            user.reset_otp=None
            user.otp_created_at=None
            user.save()
            return Response({"msg":"password rest secussful"},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        