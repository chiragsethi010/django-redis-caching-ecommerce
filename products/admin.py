from django.contrib import admin
from .models import Product
from django.core.cache import cache

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "stock", "created_at")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # 🧹 Invalidate cache on save
        cache.delete("all_products_v1")
        cache.delete(f"product:{obj.id}")

    def delete_model(self, request, obj):
        product_id = obj.id

        super().delete_model(request, obj)

        # 🧹 Invalidate cache on delete
        cache.delete("all_products_v1")
        cache.delete(f"product:{product_id}")