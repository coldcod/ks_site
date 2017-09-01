from django.shortcuts import render
from .models import Product

import sys
sys.path.append('../')
from store.models import Product

from cart.models import Cart, ProductOrder

# Create your views here.

def index(req):
    boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
    cart = Cart.objects.filter(user=req.user, session_id=None) if boolean else Cart.objects.filter(session_id=req.session.session_key, user=None)
    orders = ProductOrder.objects.filter(cart=cart)
    total = 0
    count = 0
    for order in orders:
        total += order.product.price * order.quantity
        count += order.quantity
    orders = {
        'orders': orders,
        'total': total,
        'count': count,
    }
    latest_products = Product.objects.order_by('-pubdate')
    context = {
        'latest_products': latest_products,
        'orders': orders,
    }
    return render(req, 'store/index.html', context)

def product_page(req, pid_url):
    boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
    cart = Cart.objects.filter(user=req.user, session_id=None) if boolean else Cart.objects.filter(session_id=req.session.session_key, user=None)
    orders = ProductOrder.objects.filter(cart=cart)
    total = 0
    count = 0
    for order in orders:
        total += order.product.price * order.quantity
        count += order.quantity
    cart_info = {
        'orders': orders,
        'total': total,
        'count': count,
    }
    product = Product.objects.get(pid=pid_url)
    top_message = req.GET.get('tm', '').replace('/', '')
    context = {
        'product': product,
        'image_list': product.images.all(),
        'tm': top_message,
        'cart_info': cart_info,
    }
    return render(req, 'store/product.html', context)
