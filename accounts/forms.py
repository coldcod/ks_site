from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=256, required=True)
    phone = forms.CharField()

    class Meta:
        model = User
        exclude = ['username',]
        fields = ['email', 'phone', 'password1', 'password2',]

class ProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=600)
    cc = forms.CharField(max_length=200)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=60)

    class Meta:
        model = User
        exclude = ['email_confirmed',]
        fields = ['address', 'first_name', 'last_name',]

class SellerSignupForm1(UserCreationForm):
    email = forms.EmailField(max_length=256, required=True)
    phone = forms.CharField(min_length=10)
    alternate_phone = forms.CharField(min_length=10)
    address = forms.CharField()
    name = forms.CharField()

    class Meta:
        model = User
        exclude = ['username']
        fields = ['name', 'email', 'password1', 'password2', 'phone', 'alternate_phone', 'address']

class SellerSignupForm2(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(SellerSignupForm2, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']

    name_of_your_shop = forms.CharField()
    GST_No = forms.CharField(min_length=12, max_length=12)
    PAN_No = forms.CharField(min_length=10, max_length=10)

    class Meta:
        model = User
        exclude = ['username', 'password1', 'password2']
        fields = ['name_of_your_shop', 'GST_No', 'PAN_No']

class SellerSignupForm3(UserCreationForm):
    def __init__(self, *args, **kargs):
        super(SellerSignupForm3, self).__init__(*args, **kargs)
        del self.fields['password2']
        del self.fields['password1']

    type_of_products_you_want_to_sell = forms.CharField(initial="Bakery")
    name_as_account_holder = forms.CharField()
    account_number = forms.CharField()
    IFSC_code = forms.CharField(min_length=11, max_length=11)

    class Meta:
        model = User
        exclude = ['username']
        fields = ['type_of_products_you_want_to_sell', 'name_as_account_holder', 'account_number', 'IFSC_code']
