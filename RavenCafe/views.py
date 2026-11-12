from products.models import Product, Category
from django.shortcuts import render
from decimal import Decimal


def home(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())

    cart_items = []
    cart_total = Decimal('0.000')

    cart_products = Product.objects.filter(id__in=cart.keys())

    for product in cart_products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal,
        })

        cart_total += subtotal

    return render(request, 'index.html', {
        'products': products,
        'categories': categories,
        'cart_count': cart_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
    })