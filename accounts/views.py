from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

# Create your views here.

def signup(req):
    if req.method == 'POST':
        form = UserCreationForm(req.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_psswd = form.cleaned_data.get('password1')
            user  = authenticate(username=username, password=raw_psswd)
            login(req, user)
            return redirect('store_index')
    else:
        form = UserCreationForm()
    return render(req, 'accounts/signup.html', {'form': form})
