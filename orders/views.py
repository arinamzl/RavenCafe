from django.shortcuts import redirect, get_object_or_404
from products.models import Product
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal

from products.models import Product
from .models import Order, OrderItem

def add_to_cart(request):

    if request.method == 'POST':

        product_id = request.POST.get('product_id')

        product = get_object_or_404(Product, id=product_id, available=True)

        cart = request.session.get('cart', {})

        product_id = str(product.id)

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart

    return redirect('home')

def checkout(request):

    cart = request.session.get('cart', {})

    cart_items = []
    cart_total = Decimal('0.00')

    cart_products = Product.objects.filter(
        id__in=cart.keys(),
        available=True
    )

    for product in cart_products:

        quantity = cart.get(str(product.id), 0)

        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        cart_total += subtotal

    error = None

    if request.method == 'POST':

        customer_name = request.POST.get('customer_name', '').strip()
        customer_phone = request.POST.get('customer_phone', '').strip()
        pickup_time_text = request.POST.get('pickup_time', '')

        if not cart_items:
            error = 'Your cart is empty.'

        elif not customer_name or not customer_phone:
            error = 'Please enter your name and phone number.'

        else:
            try:
                pickup_time = datetime.strptime(
                    pickup_time_text,
                    '%Y-%m-%dT%H:%M'
                )

                pickup_time = timezone.make_aware(pickup_time)

                minimum_time = timezone.now() + timedelta(minutes=30)

                if pickup_time < minimum_time:
                    error = 'Pickup time must be at least 30 minutes from now.'

            except ValueError:
                error = 'Please enter a valid pickup time.'

        if not error:
            print("CART TOTAL:", cart_total,type(cart_total))

            order = Order.objects.create(
                customer_name=customer_name,
                customer_phone=customer_phone,
                pickup_time=pickup_time,
                total_price=cart_total,
            )

            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    product_name=item['product'].name,
                    unit_price=item['product'].price,
                    quantity=item['quantity'],
                )

            request.session['cart'] = {}

            return render(request, 'checkout.html', {
                'success': True,
                'order_id': order.id,
            })

    return render(request, 'checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'error': error,
    })