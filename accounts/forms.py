from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=45, required=True)
    last_name = forms.CharField(max_length=45, required=True)
    email = forms.EmailField(max_length=256, required=True)

    class Meta:
        model = User
        exclude = ['username',]
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2',]
