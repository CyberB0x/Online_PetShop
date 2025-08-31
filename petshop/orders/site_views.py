from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import CartItem, Order, OrderItem
from django.contrib import messages
from .forms import OrderForm

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


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Ваша корзина пуста.")
        return redirect("cart")

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # переносим товары из корзины в заказ
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            # очищаем корзину
            cart_items.delete()

            messages.success(request, f"Ваш заказ №{order.id} успешно оформлен!")
            return redirect("order_success", order_id=order.id)
    else:
        form = OrderForm()

    total = sum(item.subtotal() for item in cart_items)

    return render(request, "orders/checkout.html", {
        "form": form,
        "cart_items": cart_items,
        "total": total
    })



@login_required
def checkout_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if not cart_items.exists():
        return redirect("cart")  # если корзина пустая

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()

            # переносим товары из корзины в заказ
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )
            cart_items.delete()  # очищаем корзину

            return render(request, "orders/order_success.html", {"order": order})
    else:
        form = OrderForm()

    total = sum(item.subtotal() for item in cart_items)
    return render(request, "orders/checkout.html", {"form": form, "cart_items": cart_items, "total": total})



@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "orders/order_success.html", {"order": order})
