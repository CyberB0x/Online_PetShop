from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Product, Category
from orders.forms import OrderForm
from orders.models import CartItem, Order, OrderItem
from .serializers import ProductSerializer
from rest_framework import viewsets


# главная
def home(request):
    q = request.GET.get('q') or ''
    cat = request.GET.get('cat')
    products = Product.objects.filter(is_active=True)
    if q:
        products = products.filter(name__icontains=q)
    if cat:
        products = products.filter(category_id=cat)

    categories = Category.objects.all()
    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'current_cat': int(cat) if cat else None,
        'q': q,
    })


# детальная страница товара
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'product_detail.html', {'product': product})


# корзина
@login_required(login_url='/login/')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    item, created = CartItem.objects.get_or_create(
        user=request.user, product=product, defaults={'quantity': 1}
    )
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, f"«{product.name}» добавлен в корзину.")
    return redirect('cart')


@login_required(login_url='/login/')
def cart_view(request):
    items = CartItem.objects.filter(user=request.user).select_related('product')
    total = sum(i.subtotal() for i in items)
    return render(request, "cart.html", {"cart_items": items, "total": total})


@login_required(login_url='/login/')
def update_cart(request, pk):
    if request.method == "POST":
        action = request.POST.get("action")
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False})

        if action == "increase":
            item.quantity += 1
            item.save()
        elif action == "decrease":
            item.quantity -= 1
            if item.quantity <= 0:
                item.delete()
                items = CartItem.objects.filter(user=request.user)
                total = sum(i.subtotal() for i in items)
                return JsonResponse({"success": True, "item": {"removed": True}, "cart_total": total})
            else:
                item.save()

        items = CartItem.objects.filter(user=request.user)
        total = sum(i.subtotal() for i in items)

        return JsonResponse({
            "success": True,
            "item": {"quantity": item.quantity, "total": item.subtotal()},
            "cart_total": total,
        })
    return JsonResponse({"success": False})


@login_required(login_url='/login/')
def remove_from_cart(request, pk):
    if request.method == "POST":
        try:
            item = CartItem.objects.get(pk=pk, user=request.user)
            item.delete()
        except CartItem.DoesNotExist:
            return JsonResponse({"success": False})

        items = CartItem.objects.filter(user=request.user)
        total = sum(i.subtotal() for i in items)

        return JsonResponse({"success": True, "cart_total": total})
    return JsonResponse({"success": False})


@login_required(login_url='/login/')
def checkout(request):
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

            return render(request, "order_success.html", {"order": order})
    else:
        form = OrderForm()

    total = sum(item.subtotal() for item in cart_items)
    return render(
        request,
        "checkout.html",
        {"form": form, "cart_items": cart_items, "total": total}
    )


# API (DRF)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
