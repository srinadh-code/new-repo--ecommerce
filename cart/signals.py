from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Order


#  ORDER PLACED EMAIL
@receiver(post_save, sender=Order)
def send_order_placed_email(sender, instance, created, **kwargs):
    if created:
        user = instance.user

        if not user.email:
            return

        send_mail(
            subject="Your order is placed",
            message=f"""
Hello {user.username},

   Your order has been placed successfully.

Order ID : {instance.id}
Total    : ₹{instance.total_amount}

Thank you for shopping with us.
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False
        )


#  ORDER DELETED EMAIL
@receiver(post_delete, sender=Order)
def send_order_deleted_email(sender, instance, **kwargs):
    user = instance.user

    if not user.email:
        return

    send_mail(
        subject="Your order is deleted",
        message=f"""
Hello {user.username},

 Your order has been deleted successfully.

Order ID : {instance.id}

If this was not you, please contact support.
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False
    )
