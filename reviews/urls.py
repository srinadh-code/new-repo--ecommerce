# reviews/urls.py
from django.urls import path
from .views import CreateReviewView, ProductReviewsView

urlpatterns = [
    path('add/', CreateReviewView.as_view(), name='add-review'),
    path('<int:product_id>/', ProductReviewsView.as_view(), name='product-reviews'),
]
