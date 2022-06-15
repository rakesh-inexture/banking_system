from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, AccountDetailsForm, UserAddressForm, UserLoginForm


def register_view(request):
    # here creating a register form with register_view function.
    user_form = UserRegistrationForm(request.POST or None,)
    # it will create fields like [Name, email, contact pass]
    account_form = AccountDetailsForm(request.POST or None, request.FILES or None)

    address_form = UserAddressForm(request.POST or None)

    context = {
        "title": "Create a Bank Account",
        "user_form": user_form,
        "account_form": account_form,
        "address_form": address_form,
    }

    return render(request, "accounts/register_form.html", context)

def login_view(request):
    form = UserLoginForm(request.POST or None)
    context = {"form": form,
               "title": "Load Account Details",
               }
    return render(request, "accounts/login_form.html", context)


