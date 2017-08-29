from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .forms import SignUpForm, ProfileForm
from .tokens import account_activation_token

# Create your views here.

def index(req):
    return render(req, 'accounts/index.html')

def settings(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST)
        if form.is_valid():
            user = req.user
            user.refresh_from_db()
            user.profile.cc = form.cleaned_data.get('cc')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.save()
            user.save()
            success_message = "Settings were successfuly saved."
    else:
        form = ProfileForm()
        success_message = None
    return render(req, 'accounts/settings.html', {'form': form, 'success_message': success_message})

def signup(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            raw_psswd = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            instance.username = email
            instance.save()
            instance.profile.email_confirmed = False
            login(req, instance)
            instance.profile.save()
            instance.save()
            current_site = get_current_site(req)
            message = render_to_string('accounts/activate_account_email.html', {
                'user': instance,
                'domain': current_site.domain,
                # user.pk a.k.a user.id
                'uid': urlsafe_base64_encode(force_bytes(instance.pk)),
                'token': account_activation_token.make_token(instance),
            })
            instance.email_user('Activate KS_Site Account', message)

            return redirect('account_activation_sent')
    else:
        form = SignUpForm()
    return render(req, 'accounts/signup.html', {'form': form})

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
    logout(req)
    return redirect("signup")

def account_activation_sent(req):
    return render(req, 'accounts/account_activation_sent.html')
