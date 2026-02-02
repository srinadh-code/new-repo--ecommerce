# from rest_framework import serializers
# from.models import signup

# class signupserializers(serializers.ModelSerializer):
    
#     class Meta:
#         model=signup
#         fields= ["username","email","password"]
#         password = serializers.CharField(write_only=True)
    
#     def validate_password(self, value):
#         special_char = ["@", "&", "*"]
#         for ch in special_char:
#             if ch in value:
#                 return value
#         raise serializers.ValidationError("Weak password. Add @ or & or *")

           
# class loginserializers(serializers.Serializer):
#     username=serializers.CharField()
#     password=serializers.CharField()
    
# class forgotpassword(serializers.Serializer):
#     email=serializers.EmailField()
    
# class resetpassword(serializers.Serializer):
#     email=serializers.EmailField()
#     otp=serializers.CharField(max_length=6)
#     new_password=serializers.CharField()
    
#     def validate_new_password(self,value):
#         special_character=["@","&","8"]
        
        
       # this is best practice
        # if not any(ch in value for ch in special_character):
        #     raise serializers.ValidationError("weak password")
        # return value
        
        
        # you can also write like this 
    #     if ('@' not in value) and ('&' not in value) and ('*' not in value):
         # raise serializers.ValidationError("Weak password. Add @ or & or *")

        
        # for ch in special_character:
        #     if ch in value:
        #         return value
        # raise serializers.ValidationError("weal password add @8&")
    
    
    
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Signup


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Signup
        fields = ["id", "username", "email", "password"]

    def validate_password(self, value):
        special_chars = ["@", "&", "*"]
        if not any(ch in value for ch in special_chars):
            raise serializers.ValidationError("Weak password. Add @ or & or *")
        return value

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    
    




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    new_password = serializers.CharField(write_only=True)

    def validate_new_password(self, value):
        special_chars = ["@", "&", "*"]
        if not any(ch in value for ch in special_chars):
            raise serializers.ValidationError("Weak password. Add @ or & or *")
        return value
