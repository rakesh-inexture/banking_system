from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, AccountDetails, UserAddress

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "contact_no",
            "password1",
            "password2"
        ]

class AccountDetailsForm(forms.ModelForm):
    class Meta:
        model = AccountDetails
        fields = [
            'gender',
            'birth_date',
            'picture'
        ]


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields = [
            'street_address',
            'city',
            'postal_code',
            'country'
        ]

class UserLoginForm(forms.Form):
    account_no = forms.IntegerField(label="Account Number")
    password = forms.CharField(widget=forms.PasswordInput)
