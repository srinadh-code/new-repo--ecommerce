from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=10)
    is_email_verified=models.BooleanField(default=False)
    is_phone_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
# Create your models here.
class Product(models.Model):
    Product_name=models.CharField(max_length=20)
    price=models.IntegerField()
    description=models.TextField()
    stock=models.IntegerField(default=0)
class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PLACED', 'Placed'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED','Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    order_id=models.CharField(max_length=20,unique=True)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default="PENDING")
    total_amount=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    discount_amount=models.IntegerField(default=0)


class Orderitem(models.Model):
    product_name=models.ForeignKey(Product,on_delete=models.CASCADE)
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    quatity=models.IntegerField()
    unit_price=models.IntegerField()