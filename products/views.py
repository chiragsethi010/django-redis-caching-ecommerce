from django.shortcuts import render
from .models import Product
from django.http import HttpResponse,HttpRequest,JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.cache import cache
from django_redis import get_redis_connection


def products(request):
    if request.method == 'GET':
        cache_key = "all_products_v1"
        request.cache_key = cache_key
        redis_conn = get_redis_connection("default")

        cached_data = cache.get(cache_key)

        if cached_data:
            # ✅ HIT
            redis_conn.incr("stats:hits")

            response = JsonResponse({
                "source": "cache",
                "data": cached_data
            })
            response["X-Cache"] = "HIT"
            return response

        # ❌ MISS
        redis_conn.incr("stats:misses")

        products = list(
            Product.objects.all().values(
                "id", "name", "description", "price", "stock", "created_at"
            )
        )

        cache.set(cache_key, products, 300)

        response = JsonResponse({
            "source": "database",
            "data": products
        })
        response["X-Cache"] = "MISS"
        return response




def product(request, id):
    if request.method == 'GET':
        cache_key = f"product:{id}"
        request.cache_key = cache_key 
        redis_conn = get_redis_connection("default")

        cached_product = cache.get(cache_key)

        if cached_product:
            # ✅ HIT
            redis_conn.incr("stats:hits")

            response = JsonResponse({
                "source": "cache",
                "data": cached_product
            })
            response["X-Cache"] = "HIT"
            return response

        # ❌ MISS
        redis_conn.incr("stats:misses")

        try:
            p = Product.objects.get(id=id)

            data = {
                "id": p.id,
                "name": p.name,
                "description": p.description,
                "price": str(p.price),
                "stock": p.stock,
                "created_at": p.created_at.isoformat()
            }

            cache.set(cache_key, data, 300)

            response = JsonResponse({
                "source": "database",
                "data": data
            })
            response["X-Cache"] = "MISS"
            return response

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        



@csrf_exempt
def product_update(request, id):
    if request.method in ['POST', 'PUT']:
        try:
            p = Product.objects.get(id=id)

            data = json.loads(request.body)

            # 🔄 Update fields (only if provided)
            p.name = data.get("name", p.name)
            p.description = data.get("description", p.description)
            p.price = data.get("price", p.price)
            p.stock = data.get("stock", p.stock)

            p.save()

            # 🧹 Invalidate cache
            cache.delete("all_products_v1")
            cache.delete(f"product:{id}")

            return JsonResponse({
                "message": "Product updated successfully"
            })

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
        
@csrf_exempt
def product_delete(request, id):
    if request.method == 'DELETE':
        try:
            p = Product.objects.get(id=id)
            p.delete()

            # 🧹 Invalidate cache
            cache.delete("all_products_v1")
            cache.delete(f"product:{id}")

            return JsonResponse({
                "message": "Product deleted successfully"
            })

        except Product.DoesNotExist:
            return JsonResponse({"error": "Product not found"}, status=404)
        

def cache_stats(request):
    redis_conn = get_redis_connection("default")

    hits = redis_conn.get("stats:hits")
    misses = redis_conn.get("stats:misses")

    # Convert bytes → int
    hits = int(hits) if hits else 0
    misses = int(misses) if misses else 0

    total = hits + misses

    hit_ratio = (hits / total) if total > 0 else 0

    return JsonResponse({
        "hits": hits,
        "misses": misses,
        "hit_ratio": round(hit_ratio, 2)
    })