from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=256, required=True)

    class Meta:
        model = User
        exclude = ['username',]
        fields = ['email', 'password1', 'password2',]

class ProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=600)
    cc = forms.CharField(max_length=200)

    class Meta:
        model = User
        fields = ['cc', 'address',]
