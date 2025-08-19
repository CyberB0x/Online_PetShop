from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, Category
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
def add_to_cart(request, pk):
    cart = request.session.get('cart', {})
    cart[str(pk)] = cart.get(str(pk), 0) + 1
    request.session['cart'] = cart
    messages.success(request, "The item has been added to the cart. 🛒")
    return redirect("cart")


def cart_view(request):
    cart = request.session.get('cart', {})
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    total = 0
    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.price * qty
        total += subtotal
        cart_items.append({
            "product": product,
            "qty": qty,
            "subtotal": subtotal,
        })
    return render(request, "cart.html", {"cart_items": cart_items, "total": total})


# API (DRF)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
