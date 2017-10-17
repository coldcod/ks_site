from django.shortcuts import render, redirect
from django.http import HttpResponse
from get_cart_kssite.get_cart import get_cart, get_cart_info, get_user_cart, get_session_cart
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import sys
sys.path.append('../')
from store.models import Product
from accounts.models import Profile

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

def addressFilledBuyout(req, pid):
    if req.method == 'POST':
        address = req.POST.get("address", "")
        req.user.profile.address = address
        req.user.profile.save()
        req.user.save()
        return redirect('/cart/confirmed/'+pid)

def buy(req, pid):
    boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
    if boolean is not True:
        return redirect('/accounts/login?p=' + pid)
    elif boolean:
        address_not_filled = False
        if Profile.objects.get(id=req.user.id).address == '':
            address_not_filled = True
        product = Product.objects.get(pid=pid)
        usr = req.user
        return render(req, 'cart/buy.html', {'product': product, 'usr': usr, 'address_not_filled': address_not_filled})

def confirmed(req, pid):
    boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
    if boolean and req.user.email and Profile.objects.get(id=req.user.id).address is not '':
        # To MANAGEMENT
        subject = "[ORDER]" + str(Product.objects.get(pid=pid).title)
        html_content = render_to_string('cart/order.html', {'usr': req.user, 'prod': Product.objects.get(pid=pid)})
        text_content = strip_tags(html_content)
        _from = "satwindersapra@gmail.com"
        to = "satwindersapra@gmail.com"
        msg = EmailMultiAlternatives(subject, text_content, _from, ["satwindersapra@gmail.com"])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        # To CUSTOMER
        subject = "[Order Received] " + str(Product.objects.get(pid=pid).title)
        context = {
            'no_err': True,
            'usr': req.user,
            'prod': Product.objects.get(pid=pid)
        }
        html_content = render_to_string('cart/to_cust.html', context)
        text_content = strip_tags(html_content)
        _from = "satwindersapra@gmail.com"
        to = req.user.email
        msg = EmailMultiAlternatives(subject, text_content, _from, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return render(req, 'cart/placed.html', {'prod': Product.objects.get(pid=pid)})

    else:
        return HttpResponse("Unexpected Error. Please make sure you're logged in (if not, <a class='text_links' href='/accounts/login/'>log in</a>) and try placing your order again.")
