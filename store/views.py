from django.shortcuts import render
from django.contrib.postgres.search import SearchVector
from .models import Product
from get_cart_kssite import get_cart

# Create your views here.

def index(req):
    orders = get_cart.get_cart_info(req)
    if (req.GET.get('category') is not None):
        latest_products = Product.objects.filter(category=req.GET.get('category').title())
    elif req.GET.get('q') is not None:
        latest_products = Product.objects.annotate(
            search=SearchVector('title', 'description', 'category', 'notes'),
        ).filter(search=req.GET.get('q'))
    else:
        latest_products = Product.objects.order_by('-pubdate')
    categories = Product.objects.all().values_list('category', flat=True)
    categories = list(set(categories))
    context = {
        'latest_products': latest_products,
        'cart_info': orders,
        'categories': categories,
    }
    return render(req, 'store/index.html', context)

def product_page(req, pid_url):
    cart_info = get_cart.get_cart_info(req)
    product = Product.objects.get(pid=pid_url)
    top_message = req.GET.get('tm', '').replace('/', '')
    context = {
        'product': product,
        'image_list': product.images.all(),
        'tm': top_message,
        'cart_info': cart_info,
    }
    return render(req, 'store/product.html', context)
