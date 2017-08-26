from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

from .forms import SignUpForm, ProfileForm

# Create your views here.

def index(req):
    return render(req, 'accounts/index.html')

def settings(req):
    if req.method == 'POST':
        form = ProfileForm(req.POST)
        if form.is_valid():
            # Get the logged in user from session or something, then
            '''user = user.refresh_from_db()
            user.profile.cc = form.cleaned_data.get('cc')
            user.profile.address = form.cleaned_data.get('address')
            user.profile.save()
            user.save()'''
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
            user = authenticate(username=email, password=raw_psswd, email=email)
            login(req, user)
            return redirect('store_index')
    else:
        form = SignUpForm()
    return render(req, 'accounts/signup.html', {'form': form})

def signout(req):
    logout(req)
    return redirect("signup")
