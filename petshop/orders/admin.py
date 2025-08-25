from django.contrib import admin
from .models import CartItem, Order, OrderItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity")
    search_fields = ("user__username", "product__name")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "email", "phone", "paid", "created_at")
    list_filter = ("paid", "created_at")
    search_fields = ("full_name", "email", "phone")
    inlines = [OrderItemInline]
