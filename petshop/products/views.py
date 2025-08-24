from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from orders.models import CartItem
from .serializers import ProductSerializer
from rest_framework import viewsets


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


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    return render(request, 'product_detail.html', {'product': product})


# 🛒 cart
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
    total = sum(i.product.price * i.quantity for i in items)
    return render(request, "cart.html", {"items": items, "total": total})

@login_required(login_url='/login/')
def remove_from_cart(request, pk):
    CartItem.objects.filter(pk=pk, user=request.user).delete()
    messages.info(request, "Товар удалён из корзины.")
    return redirect('cart')

# API (DRF)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
