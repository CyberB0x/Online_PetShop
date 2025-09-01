from django.db import models
from django.conf import settings
from products.models import Product

PYMENT_CHOICES = [
    ('card', 'Card'),
    ('paypal', 'Paypal'),
    ('cash', 'Cash')
]


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="orders"
    )
    full_name = models.CharField(max_length=200)
    email = models.EmailField(default="unknown@example.com")
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(max_length=255, default='Unknown')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    payment_method = models.CharField(
        max_length=20,
        choices=PYMENT_CHOICES,
        default='card'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
