from django.db import models
from django.contrib.auth.models import User
from signuplogin.models import Product   #  use Product from signuplogin


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    full_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)

    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PLACED', 'Placed'),
        ('CONFIRMED', 'Confirmed'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=20, unique=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")

    total_amount = models.IntegerField()
    discount_amount = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.order_id


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)   #  signuplogin Product
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    quantity = models.IntegerField()
    unit_price = models.IntegerField()

    def __str__(self):
        return f"{self.order.order_id} - {self.product.name}"
