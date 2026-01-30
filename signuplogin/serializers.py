from rest_framework import serializers
from.models import signup

class signupserializers(serializers.ModelSerializer):
    class Meta:
        model=signup
        fields= "__all__"
    
    def validate_password(self, value):
        special_char = ["@", "&", "*"]
        for ch in special_char:
            if ch in value:
                return value
        raise serializers.ValidationError("Weak password. Add @ or & or *")

           
class loginserializers(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
class forgotpassword(serializers.Serializer):
    email=serializers.EmailField()
    
class resetpassword(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)
    new_password=serializers.CharField()
    
    def validate_new_password(self,value):
        special_character=["@","&","8"]
        
        
       # this is best practice
        # if not any(ch in value for ch in special_character):
        #     raise serializers.ValidationError("weak password")
        # return value
        
        
        # you can also write like this 
    #     if ('@' not in value) and ('&' not in value) and ('*' not in value):
         # raise serializers.ValidationError("Weak password. Add @ or & or *")

        
        for ch in special_character:
            if ch in value:
                return value
        raise serializers.ValidationError("weal password add @8&")
    