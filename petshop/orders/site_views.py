from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Order, OrderItem
from products.models import Product

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "orders.html", {"orders": orders})

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
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            email=email,
            phone=phone,
            address=address
        )

        # переносим товары из корзины
        for product_id, qty in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, quantity=qty)

        # очищаем корзину
        request.session["cart"] = {}
        messages.success(request, "✅ Заказ успешно оформлен!")
        return redirect("order_success", order_id=order.id)

    return render(request, "checkout.html")

def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, "order_success.html", {"order": order})
