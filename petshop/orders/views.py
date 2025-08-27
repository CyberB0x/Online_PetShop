from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import JsonResponse

from .models import CartItem, Order, OrderItem
from .serializers import CartItemSerializer, OrderSerializer
from products.models import Product
from django.shortcuts import render

def orders_page(request):
    return render(request, "orders.html")

# Добавить в корзину
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity", 1)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user, product=product
    )
    if not created:
        cart_item.quantity += int(quantity)
    else:
        cart_item.quantity = quantity
    cart_item.save()

    return Response({"message": "Added to cart"})


# Удалить из корзины
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    item_id = request.data.get("item_id")
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        return Response({"message": "Removed from cart"})
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)


# Оформить заказ
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return Response({"error": "Cart is empty"}, status=400)

    order = Order.objects.create(user=request.user, total_price=0)
    total = 0
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price,
        )
        total += item.product.price * item.quantity
    order.total_price = total
    order.save()

    cart_items.delete()

    return Response({"message": "Order created", "order_id": order.id})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def update_cart(request, product_id):
    action = request.data.get("action")  # "increase" или "decrease"

    try:
        cart_item = CartItem.objects.get(user=request.user, product_id=product_id)
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"}, status=404)

    if action == "increase":
        cart_item.quantity += 1
    elif action == "decrease":
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return Response({"message": "Item removed from cart"})
    else:
        return Response({"error": "Invalid action"}, status=400)

    cart_item.save()
    return Response({"message": "Cart updated", "quantity": cart_item.quantity})


@csrf_exempt
@login_required
def update_cart(request, product_id):
    cart = request.session.get("cart", {})

    if str(product_id) not in cart:
        return JsonResponse({"error": "Item not found"}, status=400)

    action = request.POST.get("action") or request.GET.get("action")

    if action == "increase":
        cart[str(product_id)] += 1
    elif action == "decrease":
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]

    request.session["cart"] = cart
    return JsonResponse({"success": True, "cart": cart})

# Список заказов пользователя
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
