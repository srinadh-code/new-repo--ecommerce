

from rest_framework import serializers
import re
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = [
            "username",
            "email",
            "full_name",
            "phone_number",
            "address",
            "city",
            "state",
            "pincode",
            "is_email_verified",
            "is_phone_verified",
            "created_at",
        ]

        read_only_fields = [
            "is_email_verified",
            "is_phone_verified",
            "created_at",
        ]

    def validate_phone_number(self, value):
        if not re.fullmatch(r'[6-9]\d{9}', value):
            raise serializers.ValidationError("Invalid Indian phone number")
        return value
