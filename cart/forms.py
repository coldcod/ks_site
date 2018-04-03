from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class LoggedInForm(forms.ModelForm):
    address = forms.CharField(max_length=600, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=60, required=True)

    class Meta:
        model = User
        fields = ['address', 'first_name', 'last_name',]

class LoggedOutForm(forms.ModelForm):
    address = forms.CharField(max_length=600, required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=60, required=True)
    email = forms.EmailField(max_length=256, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'address']
