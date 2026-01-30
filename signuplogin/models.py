from django.db import models

class signup(models.Model):
    username=models.CharField(max_length=100)
    email=models.EmailField(max_length=254,unique=True)
    password=models.CharField(max_length=254)
    
    reset_otp=models.CharField(max_length=6,blank=True,null=True)
    otp_created_at=models.DateTimeField(blank=True,null=True)
    
    def __str__(self):
        return self.name
        
    
