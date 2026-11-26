from django.db import models


class Order(models.Model):

    customer_name = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=20)

    pickup_time = models.DateTimeField()

    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Order {self.id} - {self.customer_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.SET_NULL,
        null=True
    )

    product_name = models.CharField(max_length=100)

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField()

    def str(self):
        return f"{self.product_name} x {self.quantity}"