from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from get_cart_kssite import get_cart
from django.contrib.auth.models import Permission

from .forms import SignUpForm, ProfileForm, SellerSignupForm1, SellerSignupForm2, SellerSignupForm3
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
        'uid': urlsafe_base64_encode(force_bytes(instance.pk)).decode(),
        'token': account_activation_token.make_token(instance),
    })
    send_mail("Activate Your Account | The Decorista", message, "TheDecorista.in@gmail.com", [instance.email])
    #msg = EmailMultiAlternatives("Activate The Decorista Account", message, "satwindersapra@gmail.com", [instance.email])
    #msg.send()
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

                # --- Adding permissions for normally signing up users to access admin page and list, edit their products ---

                """instance.is_staff = True

                permission = Permission.objects.get(name='Can add product')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can change product')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can delete product')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can add product images')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can change product images')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can delete product images')
                instance.user_permissions.add(permission)"""

                # --- end of permissions ---

                instance.profile.email_confirmed = False
                instance.profile.phone_number = pno
                instance.profile.save()
                instance.save()
                login(req, instance)
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

def seller(req):
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
    return render(req, 'accounts/seller.html', context)

def seller_signup1(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    form = SellerSignupForm1()
    context = {
        'form': form,
        'cart_info': cart_info,
        'orders': orders,
        'total': orders['total'] or 0,
        'count': orders['count'] or 0,
        'categories': categories,
    }
    return render(req, 'accounts/seller/signup1.html', context)

def seller_signup2(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    if req.method == 'POST':
        form = SellerSignupForm1(req.POST)
        if form.is_valid():
            try:
                instance = form.save(commit=False)
                raw_psswd = form.cleaned_data.get('password2')
                email = form.cleaned_data.get('email')
                pno = form.cleaned_data.get('phone')
                name = form.cleaned_data.get('name')
                alt_phone = form.cleaned_data.get('alternate_phone')
                address = form.cleaned_data.get('address')
                instance.username = email
                instance.save()

                # --- Adding permissions for signing up sellers to access admin page and list, edit their products ---

                instance.is_staff = True

                permission = Permission.objects.get(name='Can add product')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can change product')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can delete product')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can add product images')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can change product images')
                instance.user_permissions.add(permission)

                permission = Permission.objects.get(name='Can delete product images')
                instance.user_permissions.add(permission)

                # --- end of permissions ---

                instance.profile.email_confirmed = True
                instance.profile.phone_number = pno
                instance.profile.alt_phone_number = alt_phone
                instance.profile.name = name
                instance.email = email
                instance.profile.address = address

                login(req, instance)
                instance.profile.save()
                instance.save()
            except Exception as e:
                return render(req, 'accounts/seller/signup1.html', {'form': form, 'tm': "Email already registered."})

        form = SellerSignupForm2()
        context = {
            'form': form,
            'cart_info': cart_info,
            'orders': orders,
            'total': orders['total'] or 0,
            'count': orders['count'] or 0,
            'categories': categories,
        }
        return render(req, 'accounts/seller/signup2.html', context)

    else:
        return redirect('store_index')

def seller_signup3(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    if req.method == 'POST':
        form = SellerSignupForm2(req.POST)
        if form.is_valid():
            try:
                req.user.profile.shopname = form.cleaned_data.get('name_of_your_shop')
                req.user.profile.gst = form.cleaned_data.get('GST_No')
                req.user.profile.pan = form.cleaned_data.get('PAN_No')
                req.user.profile.save()
                req.user.save()
            except Exception as e:
                return HttpResponse("An error has occured. Please contact for support.")

        form = SellerSignupForm3()
        context = {
            'form': form,
            'cart_info': cart_info,
            'orders': orders,
            'total': orders['total'] or 0,
            'count': orders['count'] or 0,
            'categories': categories,
        }
        return render(req, 'accounts/seller/signup3.html', context)

    else:
        return redirect('store_index')

def seller_signup4(req):
    orders = get_cart.get_cart_info(req)
    categories = list(set(Product.objects.all().values_list('category', flat=True)))
    cart_info = get_cart.get_cart_info(req)
    if req.method == 'POST':
        form = SellerSignupForm3(req.POST)
        if form.is_valid():
            try:
                req.user.profile.prodtype = form.cleaned_data.get('type_of_products_you_want_to_sell')
                req.user.profile.accountholder = form.cleaned_data.get('name_as_account_holder')
                req.user.profile.account_number = form.cleaned_data.get('account_number')
                req.user.profile.IFSC_code = form.cleaned_data.get('IFSC_code')
                req.user.profile.save()
                req.user.save()
            except Exception as e:
                return HttpResponse("An error has occured. Please contact for support.")

        return HttpResponseRedirect('/admin/')

    else:
        return redirect('store_index')

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
