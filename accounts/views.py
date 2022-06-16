from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, AccountDetailsForm, UserAddressForm, UserLoginForm

def register_view(request):
    # here creating a register form with register_view function.
    if request.user.is_authenticated:
        return redirect("home:home_view")
    else:
        user_form = UserRegistrationForm(request.POST or None,)
        account_form = AccountDetailsForm(request.POST or None, request.FILES or None)
        address_form = UserAddressForm(request.POST or None)

        if user_form.is_valid() and account_form.is_valid() and address_form.is_valid():
            # here I am getting most of model data from a form,
            # but I need to populate some null=False fields with non-form data.
            user = user_form.save(commit=False)
            account_details = account_form.save(commit=False)
            address = address_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            account_details.user = user
            account_details.save()
            address.user = user
            address.save()
            new_user = authenticate(
                account_no=user.account_no, password=password
            )
            login(
                request, new_user, backend='accounts.backends.AccountNoBackend'
            )
            messages.success(
                request,
                '''Thank You For Creating A Bank Account {}.
                Your Account Number is {}, Please use this number to login
                '''.format(new_user.full_name, new_user.account_no))

            return redirect("home:home_view")

        context = {
        "title": "Create a Bank Account",
        "user_form": user_form,
        "account_form": account_form,
        "address_form": address_form,
        }

        return render(request, "accounts/register_form.html", context)

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home:home_view")
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            account_no = form.cleaned_data.get("account_no")
            password = form.cleaned_data.get("password")
            # authenticate with Account No & Password
            user = authenticate(account_no=account_no, password=password)
            login(request, user, backend='accounts.backends.AccountNoBackend')
            messages.success(request, 'Welcome, {}!'.format(user.full_name))
            return redirect("home:home_view")

        context = {"form": form,
               "title": "Load Account Details via Login",
               }
        return render(request, "accounts/login_form.html", context)

def logout_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    else:
        logout(request)
        return redirect("home:home_view")