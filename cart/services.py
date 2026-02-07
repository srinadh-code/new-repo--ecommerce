from .models import CartItem


def count(user):
    if not user.is_authenticated:
        return 0
    return CartItem.objects.filter(user=user).count()