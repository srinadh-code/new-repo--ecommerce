from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10)
    is_email_verifield=models.BooleanField(default=False)
    is_phone_verified=models.BooleanField(default=False)
    create_at=models.DateTimeField(auto_now_add=True)
    updates_At=models.DateTimeField(auto_now=True)
# Create your models here.
