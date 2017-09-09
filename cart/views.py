from django.shortcuts import render, redirect
from get_cart_kssite.get_cart import get_cart, get_cart_info, get_user_cart, get_session_cart

# Create your views here.

def add_to_cart(req, pid):
    cart = get_cart(req)
    cart._add(pid)
    return redirect('/store/' + pid + "/?tm=Added+to+cart/")

def remove_from_cart(req, pid):
    cart = get_cart(req)
    cart._remove(pid)
    return redirect('/store/' + pid + '/?tm=Removed+from+cart/')

def cart(req):
    user_cart = get_user_cart(req)
    session_cart = get_session_cart(req)
    cart_info = get_cart_info(req)
    context = {
        'user_cart': user_cart,
        'session_cart': session_cart,
        'orders': cart_info['orders'],
        'total': cart_info['total'],
        'count': cart_info['count'],
    }
    return render(req, 'cart/cart-info.html', context)
