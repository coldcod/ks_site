from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from get_cart_kssite.get_cart import get_cart, get_cart_info, get_user_cart, get_session_cart
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from instamojo_wrapper import Instamojo
import sys
sys.path.append('../')
from cart.models import Cart
from store.models import Product
from accounts.models import Profile

API_KEY = settings.API_KEY
AUTH_TOKEN = settings.AUTH_TOKEN

api = Instamojo(api_key=API_KEY, auth_token=AUTH_TOKEN, endpoint='https://www.instamojo.com/@Decorista/')

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
    orders = get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart_info(req)
    user_cart = get_user_cart(req)
    session_cart = get_session_cart(req)
    cart_info = get_cart_info(req)
    address_not_filled = req.user.profile.address == '' if req.user.is_authenticated() else ''
    first_name_not_filled = req.user.first_name == '' if req.user.is_authenticated() else ''
    last_name_not_filled = req.user.last_name == '' if req.user.is_authenticated() else ''
    context = {
        'cart_info': cart_info,
        'categories': categories,
        'user_cart': user_cart,
        'session_cart': session_cart,
        'orders': cart_info['orders'],
        'total': cart_info['total'] or 0,
        'count': cart_info['count'] or 0,
        'address_not_filled': address_not_filled,
        'first_name_not_filled': first_name_not_filled,
        'last_name_not_filled': last_name_not_filled,
        'usr': req.user,
        'authenticated': req.user.is_authenticated()
    }
    return render(req, 'cart/cart-info.html', context)

def addressFilledBuyout(req):
    if req.method == 'POST':
        req.user.profile.address = req.POST.get("address", '')
        req.user.first_name = req.POST.get("first_name", '')
        req.user.last_name = req.POST.get("last_name", '')
        req.user.profile.save()
        req.user.save()
    pid = "?p=" + str(req.GET.get('p')) if req.GET.get('p') else '/'
    # return redirect('/cart/confirmed'+pid)
    prod = Product.objects.get(pid=str(req.GET.get('p')).replace('/', '') )
    purpose = prod.title
    fname = req.user.first_name
    lname = req.user.last_name
    fullname = fname + ' ' + lname
    amount = prod.price
    response = api.payment_request_create(
        amount = amount,
        purpose = purpose,
        send_email = False,
        buyer_name = fullname,
        redirect_url = req.build_absolute_uri('admin')
    )
    return HttpResponseRedirect(response['payment_request']['longurl'])

def confirmed(req):
    orders = get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart_info(req)
    pid = req.GET.get('p' '')
    '''if req.GET.get('p') is not '' or req.GET.get('p') is not NoneType:
        pid = req.GET.get('p').replace('/', '')
    else:
        pid = None'''
    boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"


    # Taking orders from guests
    if req.method == 'POST':
        address = req.POST.get('address')
        first_name = req.POST.get('first_name')
        last_name = req.POST.get('last_name')
        email = req.POST.get('email')

        # To MANAGEMENT
        subject = "[TD_ORDER] " + str(Product.objects.get(pid=pid.replace('/', '')).title) if pid else "[ORDER] Various Products"
        prod = Product.objects.get(pid=pid.replace('/', '')) if pid is not '' and pid is not None else None
        author_email = prod.author.email if prod else ''
        orders = None if pid is not '' and pid is not None else get_cart_info(req)

        # If order has only one product
        if prod is not None and prod is not '':
            context = {
                'usr': req.user,
                'address': address,
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'prod': prod,
                'orders': '',
                'logged_in': False
            }
            html_content = render_to_string('cart/order.html', context)
            text_content = strip_tags(html_content)
            _from = "TheDecorista.in@gmail.com"
            send_mail(subject, text_content, _from, [author_email])

        # If order has more than 1 product
        elif orders and orders is not '':
            for order in orders['orders']:
                context = {
                    'usr': req.user,
                    'address': address,
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'prod': order.product,
                    'orders': '',
                    'logged_in': False
                }
                html_content = render_to_string('cart/order.html', context)
                text_content = strip_tags(html_content)
                _from = "TheDecorista.in@gmail.com"
                subject = "[TD_ORDER] " + str(order.product.title)
                send_mail(subject, text_content, _from, [order.product.author.email])

        # To CUSTOMER
        subject = "[Order Received] " + str(Product.objects.get(pid=pid.replace('/', '')).title) if pid else "[Order Received] Various Products"
        context = {
            'no_err': True,
            'usr': req.user,
            'address': address,
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'prod': prod,
            'orders': orders,
            'logged_in': False
        }
        html_content = render_to_string('cart/to_cust.html', context)
        text_content = strip_tags(html_content)
        _from = "TheDecorista.in@gmail.com"
        send_mail(subject, text_content, _from, [email])

        if prod is '' or prod is None:
            cart = get_cart(req)
            for order in orders['orders']:
                cart._remove(order.product.pid)

        context = {
            'cart_info': cart_info,
            'orders': orders,
            'total': 0,
            'count': 0,
            'categories': categories,
        }
        return render(req, 'cart/placed.html', context)

    # Taking orders from logged in and valid users
    if boolean and req.user.email and req.user.profile.address is not '' and req.user.first_name is not '' and req.user.last_name is not '':
        # To MANAGEMENT
        subject = "[ORDER] " + str(Product.objects.get(pid=pid.replace('/', '')).title) if pid else "[ORDER] Various Products"
        prod = Product.objects.get(pid=pid.replace('/', '')) if pid is not '' and pid is not None else None
        orders = None if pid is not '' and pid is not None else get_cart_info(req)

        # If order has 1 Product
        if prod is not None and prod is not '':
            context = {
                'usr': req.user,
                'prod': prod,
                'orders': '',
                'logged_in': True
            }
            html_content = render_to_string('cart/order.html', context)
            text_content = strip_tags(html_content)
            _from = "TheDecorista.in@gmail.com"
            send_mail(subject, text_content, _from, [prod.author.email])

        # If order has >1 prods
        if orders is not None and orders is not '':
            for order in orders['orders']:
                context = {
                    'usr': req.user,
                    'prod': order.product,
                    'orders': '',
                    'logged_in': True
                }
                html_content = render_to_string('cart/order.html', context)
                text_content = strip_tags(html_content)
                _from = "TheDecorista.in@gmail.com"
                subject = "[TD_ORDER] " + str(order.product.title)
                send_mail(subject, text_content, _from, [order.product.author.email])

        # To CUSTOMER
        subject = "[Order Received] " + str(Product.objects.get(pid=pid.replace('/', '')).title) if pid else "[Order Received] Various Products"
        context = {
            'no_err': True,
            'usr': req.user,
            'prod': prod,
            'orders': orders,
            'logged_in': True
        }
        html_content = render_to_string('cart/to_cust.html', context)
        text_content = strip_tags(html_content)
        _from = "TheDecorista.in@gmail.com"
        to = req.user.email
        send_mail(subject, text_content, _from, [to])

        if prod is '' or prod is None:
            cart = get_cart(req)
            for order in orders['orders']:
                cart._remove(order.product.pid)

        context = {
            'cart_info': cart_info,
            'orders': orders,
            'total': 0,
            'count': 0,
            'categories': categories,
        }
        return render(req, 'cart/placed.html', context)

    else:
        return HttpResponse("Unexpected Error. Please make sure you're logged in (if not, <a class='text_links' href='/accounts/login/'>log in</a>), have filled out your first and last name as well as address (<a class='text_links' href='/accounts/settings/'>Settings</a>) and try placing your order again.")

@csrf_exempt
def buy(req):
    orders = get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart_info(req)
    pid = req.GET.get('p', '')
    boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
    if boolean is not True:
        product = Product.objects.get(pid=pid)
        usr = req.user
        context = {
            'usr': usr,
            'product': product,
            'logged_in': False,
            'cart_info': cart_info,
            'orders': orders,
            'total': orders['total'] or 0,
            'count': orders['count'] or 0,
            'categories': categories,
        }
        return render(req, 'cart/buy.html', context)
    elif boolean:
        address_not_filled = req.user.profile.address == ''
        first_name_not_filled = req.user.first_name == ''
        last_name_not_filled = req.user.last_name == ''
        product = Product.objects.get(pid=pid)
        usr = req.user
        context = {
            'usr': usr,
            'product': product,
            'logged_in': True,
            'address_not_filled': address_not_filled,
            'first_name_not_filled': first_name_not_filled,
            'last_name_not_filled': last_name_not_filled,
            'cart_info': cart_info,
            'orders': orders,
            'total': orders['total'] or 0,
            'count': orders['count'] or 0,
            'categories': categories,
        }
        return render(req, 'cart/buy.html', context)
