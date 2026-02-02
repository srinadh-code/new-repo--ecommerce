# from django.db import models

# class signup(models.Model):
#     username=models.CharField(max_length=100)
#     email=models.EmailField(max_length=254,unique=True)
#     password=models.CharField(max_length=254)
    
#     reset_otp=models.CharField(max_length=6,blank=True,null=True)
#     otp_created_at=models.DateTimeField(blank=True,null=True)
    
#     def __str__(self):
#         return self.name
        
    
from django.db import models
from django.utils import timezone


class Signup(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(Signup, on_delete=models.CASCADE, related_name="otps")
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - {self.otp}"
from django.db import models

class Banner(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="banners/")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title if self.title else "Banner"
