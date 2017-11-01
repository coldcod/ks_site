from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from get_cart_kssite import get_cart

from .forms import SignUpForm, ProfileForm
from .tokens import account_activation_token

import sys
sys.path.append('../')
from store.models import Product

from cart.models import Cart, ProductOrder


# Create your views here.

def xyz(req):
    req.session['xyz'] = "Multi-tab session test"
    req.user.email = 'user-accross-tabs@a.com'
    return HttpResponse(str(req.user.is_anonymous) + str(req.user.email) + "<br><a href='/accounts/abc/'>abc</a>")

def abc(req):
    req.session.save()
    '''boolean = req.user.is_authenticated() and str(req.user.is_anonymous) == "CallableBool(False)"
    cart, created = Cart.objects.get_or_create(user=req.user, defaults={'session_id': req.session.session_key, 'user': req.user}) if boolean else Cart.objects.get_or_create(session_id=req.session.session_key, defaults={'session_id': req.session.session_key})
    cart.save()'''
    return HttpResponse(str(req.session.session_key))

def index(req):
    return render(req, 'accounts/index.html')

def settings(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    if req.method == 'POST':
        form = ProfileForm(req.POST)
        if form.is_valid():
            user = req.user
            user.refresh_from_db()
            user.profile.cc = req.POST.get('cc')
            user.profile.address = req.POST.get('address')
            user.first_name = req.POST.get('first_name')
            user.last_name = req.POST.get('last_name')
            user.profile.save()
            user.save()
            success_message = "Settings were successfuly saved."
        else:
            success_message = "Form was rendered invalid. Please fill the form with appropriate information."
    else:
        form = ProfileForm()
        success_message = None
    context = {
        'cart_info': cart_info,
        'orders': orders,
        'total': orders['total'] or 0,
        'count': orders['count'] or 0,
        'categories': categories,
        'user': req.user,
        'success_message': success_message,
    }
    return render(req, 'accounts/settings.html', context)

def send_activation_email(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    instance = req.user
    current_site = get_current_site(req)
    # --- #
    message = render_to_string('accounts/activate_account_email.html', {
        'user': instance,
        'domain': current_site.domain,
        # user.pk a.k.a user.id
        'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
        'token': account_activation_token.make_token(instance),
    })
    msg = EmailMultiAlternatives("Activate KS_Mart account", message, "satwindersapra@gmail.com", [instance.email])
    msg.send()
    return redirect('account_activation_sent')

def signup(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                raw_psswd = form.cleaned_data.get('password2')
                email = form.cleaned_data.get('email')
                pno = form.cleaned_data.get('phone')
                instance.username = email
                instance.save()
                instance.profile.email_confirmed = False
                instance.profile.phone_number = pno
                login(req, instance)
                instance.profile.save()
                instance.save()

                return redirect('send_activation_email')
            except Exception as e:
                return render(req, 'accounts/signup.html', {'form': form, 'tm': "Email already registered."})
    else:
        form = SignUpForm()
    context = {
        'form': form,
        'cart_info': cart_info,
        'orders': orders,
        'total': orders['total'] or 0,
        'count': orders['count'] or 0,
        'categories': categories,
    }
    return render(req, 'accounts/signup.html', context)

def activate(req, uid, token):
    uid = force_text(urlsafe_base64_decode(uid))
    user = User.objects.get(pk=uid)

    if ((user != None) and account_activation_token.check_token(user, token)):
        user.is_active = True
        user.profile.email_confirmed = True
        user.profile.save()
        user.save()
        login(req, user)
        # HOWTO: pass context through 'redirect' function i.e. {'header_message': 'Account activated.'}
        return redirect('store_index')
    else:
        return render(req, 'accounts/account_activation_invalid.html')

def signout(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    logout(req)
    return redirect("signup")

def account_activation_sent(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    context = {
        'cart_info': cart_info,
        'orders': orders,
        'total': orders['total'] or 0,
        'count': orders['count'] or 0,
        'categories': categories,
    }
    return render(req, 'accounts/account_activation_sent.html', context)
