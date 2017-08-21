from django.shortcuts import render
from .models import Product

# Create your views here.

def index(req):
    latest_products = Product.objects.order_by('-pubdate')
    context = {
        'latest_products': latest_products,
    }
    return render(req, 'store/index.html', context)

def product_page(req, pid_url):
    product = Product.objects.get(pid=pid_url)
    context = {
        'product': product,
        'image_list': product.images.all()
    }
    return render(req, 'store/product.html', context)
