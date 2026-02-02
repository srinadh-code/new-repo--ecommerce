from rest_framework import serializers
from .models import Profile
import re

class ProfileSerializer(serializers.ModelSerializer):
    def validate_phone_number(self,value):
        if not re.match(r'^[6-9]\d{9}$',value):
            raise serializers.ValidationError(
                "invalid Indian phone number"
            )
        return value
        
    class Meta:
        model=Profile
        fields=['full_name','phone_number']