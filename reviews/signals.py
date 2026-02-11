# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from django.db.models import Avg
# from .models import Review


# @receiver([post_save, post_delete], sender=Review)
# def update_product_rating(sender, instance, **kwargs):
#     product = instance.product
#     reviews = product.reviews.all()

#     product.total_reviews = reviews.count()
#     product.average_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
#     product.save(update_fields=['average_rating', 'total_reviews'])
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review


@receiver(post_save, sender=Review)
def update_product_rating_on_save(sender, instance, **kwargs):
    print("Signal Triggered")

    product = instance.product
    reviews = product.reviews.all()

    product.total_reviews = reviews.count()
    product.average_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg'] or 0

    product.save(update_fields=['total_reviews', 'average_rating'])


@receiver(post_delete, sender=Review)
def update_product_rating_on_delete(sender, instance, **kwargs):
    product = instance.product
    reviews = product.reviews.all()

    product.total_reviews = reviews.count()
    product.average_rating = reviews.aggregate(
        Avg('rating')
    )['rating__avg'] or 0

    product.save(update_fields=['total_reviews', 'average_rating'])
