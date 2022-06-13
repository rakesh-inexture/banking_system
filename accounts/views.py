from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, AccountDetailsForm, UserAddressForm

def register_view(request):
    user_form = UserRegistrationForm(
        request.POST or None,
    )
    account_form = AccountDetailsForm(
        request.POST or None,
        request.FILES or None
    )
    address_form = UserAddressForm(
        request.POST or None
    )

    context = {
        "title": "Create a Bank Account",
        "user_form": user_form,
        "account_form": account_form,
        "address_form": address_form,
    }

    return render(request, "accounts/register_form.html", context)


