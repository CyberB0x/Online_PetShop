from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from products.models import Product


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders.html", {"orders": orders})


@login_required
def checkout(request):
    cart = request.session.get("cart", {})
    if not cart:
        messages.warning(request, "Корзина пуста 🛒")
        return redirect("cart")

    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address
        )

        # переносим товары из корзины
        for product_id, qty in cart.items():
            product = get_object_or_404(Product, id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=qty)

        # очищаем корзину
        request.session["cart"] = {}
        messages.success(request, "✅ Заказ успешно оформлен!")
        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html")


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, "order_success.html", {"order": order})


@login_required
def cart_item(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0

    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.price * qty
        cart_items.append({"product": product, "qty": qty, "subtotal": subtotal})
        total += subtotal

    return render(request, "cart.html", {"cart_items": cart_items, "total": total})


@login_required
def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session["cart"] = cart
    messages.success(request, "Товар добавлен в корзину")
    return redirect("cart")


@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session["cart"] = cart
        messages.info(request, "Товар удален из корзины")
    return redirect("cart")


@login_required
def update_cart(request, product_id):
    cart = request.session.get("cart", {})
    if str(product_id) not in cart:
        return JsonResponse({"success": False, "error": "not_in_cart"}, status=400)

    action = request.POST.get("action")
    removed = False

    if action == "increase":
        cart[str(product_id)] += 1
    elif action == "decrease":
        if cart[str(product_id)] > 1:
            cart[str(product_id)] -= 1
        else:
            del cart[str(product_id)]
            removed = True

    request.session["cart"] = cart

    # обновляем общую сумму
    products = Product.objects.filter(id__in=cart.keys())
    cart_total = sum(p.price * cart[str(p.id)] for p in products)

    if removed:
        return JsonResponse({
            "success": True,
            "item": {
                "quantity": 0,
                "total": 0,
                "removed": True
            },
            "cart_total": cart_total
        })

    # если товар остался в корзине
    product = Product.objects.get(id=product_id)
    return JsonResponse({
        "success": True,
        "item": {
            "quantity": cart[str(product_id)],
            "total": cart[str(product_id)] * product.price,
            "removed": False
        },
        "cart_total": cart_total
    })