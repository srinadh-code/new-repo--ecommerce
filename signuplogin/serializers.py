from rest_framework import serializers

# class SignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = Signup
#         fields = ["id", "username", "email", "password"]

#     def validate_password(self, value):
#         special_chars = ["@", "&", "*","!","#","^","$"]
#         if not any(ch in value for ch in special_chars):
#             raise serializers.ValidationError("Weak password.ad  any special character")
#         return value

#     def create(self, validated_data):
#         validated_data["password"] = make_password(validated_data["password"])
#         return super().create(validated_data)
    




# class SignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     confirm_password = serializers.CharField(write_only=True)   #  new field

#     class Meta:
#         model = Signup
#         fields = ["id", "username", "email", "password", "confirm_password"]

#     def validate_password(self, value):
#         special_chars = ["@", "&", "*", "!", "#", "^", "$"]
#         if not any(ch in value for ch in special_chars):
#             raise serializers.ValidationError("Weak password. Add any special character")
#         return value

#     def validate(self, data):
#         #  check both passwords match
#         if data["password"] != data["confirm_password"]:
#             raise serializers.ValidationError({"confirm_password": "Passwords do not match"})
#         return data

#     def create(self, validated_data):
#         # remove confirm_password before saving
#         validated_data.pop("confirm_password")

#         #  hash password before saving
#         validated_data["password"] = make_password(validated_data["password"])
#         return super().create(validated_data)


# serializers.py
from django.contrib.auth.models import User


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )


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
