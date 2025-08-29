from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import CartItem

@login_required
def checkout(request):
    pass

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal for item in cart_items)
    return render(request, "orders/cart.html", {"cart_items": cart_items, "total": total})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,  # ВАЖНО!
        product=product
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")

@login_required
def update_cart(request, item_id):
    if request.method == "POST":
        action = request.POST.get("action")
        item = get_object_or_404(CartItem, id=item_id, user=request.user)

        if action == "increase":
            item.quantity += 1
        elif action == "decrease":
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
                cart_total = sum(i.subtotal for i in CartItem.objects.filter(user=request.user))
                return JsonResponse({"success": True, "item": {"removed": True}, "cart_total": cart_total})

        item.save()
        cart_total = sum(i.subtotal for i in CartItem.objects.filter(user=request.user))
        return JsonResponse({"success": True, "item": {"quantity": item.quantity, "total": item.subtotal}, "cart_total": cart_total})

    return JsonResponse({"success": False})


@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=item_id, user=request.user)
        item.delete()
        cart_total = sum(i.subtotal for i in CartItem.objects.filter(user=request.user))
        return JsonResponse({"success": True, "cart_total": cart_total})

    return JsonResponse({"success": False})
