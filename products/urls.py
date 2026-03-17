from django.contrib import admin
from django.urls import path
from .views import products,product
from . import views
urlpatterns = [
    path('products/', products),
    path('product/<int:id>',product),
        # ✏️ Update Product
    path('product/<int:id>/update/', views.product_update, name='product_update'),

    # 🗑️ Delete Product
    path('product/<int:id>/delete/', views.product_delete, name='product_delete'),
    path('cache-stats/', views.cache_stats, name='cache_stats'),
]