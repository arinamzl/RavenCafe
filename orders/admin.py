from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer_name',
        'customer_phone',
        'pickup_time',
        'total_price',
        'created_at',
    )

    list_filter = ('pickup_time',)
    search_fields = ('customer_name', 'customer_phone')

    inlines = [OrderItemInline]