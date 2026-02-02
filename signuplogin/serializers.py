from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Signup


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Signup
        fields = ["id", "username", "email", "password"]

    def validate_password(self, value):
        special_chars = ["@", "&", "*","!","#","^","$"]
        if not any(ch in value for ch in special_chars):
            raise serializers.ValidationError("Weak password.ad  any special character")
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
        special_chars =["@", "&", "*","!","#","^","$"]
        if not any(ch in value for ch in special_chars):
            raise serializers.ValidationError("Weak password. any special characters")
        return value
