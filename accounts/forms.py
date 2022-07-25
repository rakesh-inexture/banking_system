from .models import User, AccountDetails, AddressDetails, District
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
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
            'account_type',
            'gender',
            'birth_date',
            'picture'
        ]


class AddressDetailsForm(forms.ModelForm):
    class Meta:
        model = AddressDetails
        fields = [
            'street_address',
            'postal_code',
            'state',
            'district',
            'branch_name',
        ]

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['district'].queryset = District.objects.none()

            if 'state' in self.data:
                try:
                    state_id = int(self.data.get('state'))
                    self.fields['districts'].queryset = District.objects.filter(state_id=state_id).order_by('name')
                except (ValueError, TypeError):
                    pass  # invalid input from the client; ignore and fallback to empty City queryset
            elif self.instance.pk:
                self.fields['district'].queryset = self.instance.state.district_set.order_by('name')


class UserLoginForm(forms.Form):
    account_no = forms.IntegerField(label="Account Number")
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        account_no = self.cleaned_data.get("account_no")
        password = self.cleaned_data.get("password")

        if account_no and password:
            user = authenticate(account_no=account_no, password=password)
            if not user:
                raise forms.ValidationError("Login Credentials is not Valid")
            if not user.check_password(password):
                raise forms.ValidationError("Password Does not Match.")
            if not user.is_active:
                raise forms.ValidationError("Account is not Active.")

        return super(UserLoginForm, self).clean(*args, **kwargs)
