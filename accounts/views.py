from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import SignUpForm

# Create your views here.

def index(req):
    return render(req, 'accounts/index.html')

def signup(req):
    if req.method == 'POST':
        form = SignUpForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_psswd = form.cleaned_data.get('password2')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = authenticate(username=email, password=raw_psswd, email=email, first_name=first_name, last_name=last_name)
            login(req, user)
            return redirect('store_index')
    else:
        form = SignUpForm()
    return render(req, 'accounts/signup.html', {'form': form})

def signout(req):
    logout(req)
    return redirect("signup")
