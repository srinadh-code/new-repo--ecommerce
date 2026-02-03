from django.contrib import admin
from .models import Banner
from .models import Category, Product
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "is_active")

admin.site.register(Category)
admin.site.register(Product)
