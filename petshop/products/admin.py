from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "category", "is_active", "created_at", "image_tag")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    readonly_fields = ("image_tag",)

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:8px;"/>', obj.image.url)
        return "—"
    image_tag.short_description = "Image"
