from django.shortcuts import redirect, get_object_or_404
from products.models import Product


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