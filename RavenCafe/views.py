from products.models import Product, Category
from django.shortcuts import render

def home(request):
    products= Product.objects.filter(available=True)
    categories = Category.objects.all()
    return render(request, 'index.html', {'products': products, 'categories': categories})

