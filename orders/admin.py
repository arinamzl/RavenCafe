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
        'phone_number',
        'pickup_time',
        'total_price',
        'status',
    )

    list_filter = ('status', 'pickup_time')
    search_fields = ('customer_name', 'phone_number')

    inlines = [OrderItemInline]