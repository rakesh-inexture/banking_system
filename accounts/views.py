import json
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts import forms
from django.views import View
from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import User, District, Branch, AccountDetails, UserAddress

class RegisterView(View):
    def get(self, request):
        # here creating a register form with register_view function.
        if request.user.is_authenticated:
            return redirect("user_profile")
        else:
            user_form = forms.UserRegistrationForm()
            account_form = forms.AccountDetailsForm()
            address_form = forms.UserAddressForm()

            context = {
            "title": "Create a Bank Account",
            "user_form": user_form,
            "account_form": account_form,
            "address_form": address_form,
            }
            return render(request, "accounts/register_form.html", context)

    def post(self, request):
        user_form = forms.UserRegistrationForm(request.POST or None, )
        account_form = forms.AccountDetailsForm(request.POST or None, request.FILES or None)
        address_form = forms.UserAddressForm(request.POST or None)

        if user_form.is_valid() and account_form.is_valid() and address_form.is_valid():
            # here I am getting most of model data from a form,
            # but I need to populate some null=False fields with non-form data.
            user_details = user_form.save(commit=False)
            account_details = account_form.save(commit=False)
            address_details = address_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user_details.set_password(password)
            user_details.save()
            account_details.user = user_details
            account_details.save()
            address_details.user = user_details
            address_details.save()
            new_user = authenticate(account_no=user_details.account_no, password=password)
            login(request, new_user, backend='accounts.backends.AccountNoBackend')

            messages.success(request, '''Thank You For Creating A Bank Account {}.
                Your Account Number is {}, Please use this number to login
                '''.format(new_user.full_name, new_user.account_no))
            return redirect("user_profile")

        context = {
            "title": "Create a Bank Account",
            "user_form": user_form,
            "account_form": account_form,
            "address_form": address_form,
        }
        return render(request, "accounts/register_form.html", context)

class LoadDistrictsView(View):
    def get(self, request):
        state_id = request.GET.get('state_id')
        districts = District.objects.filter(state_id=state_id).order_by('district_name')
        filtered_districts = {district.id: district.district_name for district in districts}
        return HttpResponse(json.dumps(filtered_districts))

class LoadBranchView(View):
    def get(self, request):
        district_id = request.GET.get('district_id')
        branches = Branch.objects.filter(district_id=district_id).order_by('branch_name')
        filtered_branches = {branch.id: branch.branch_name for branch in branches}
        return HttpResponse(json.dumps(filtered_branches))

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("user_profile")
        else:
            form = forms.UserLoginForm()
            context = {"form": form,
                   "title": "Load Account Details via Login",
                   }
            return render(request, "accounts/login_form.html", context)

    def post(self, request):
        form = forms.UserLoginForm(request.POST)
        if form.is_valid():
            account_no = form.cleaned_data.get("account_no")
            password = form.cleaned_data.get("password")
            # authenticate with Account No & Password
            user = authenticate(account_no=account_no, password=password)
            login(request, user, backend='accounts.backends.AccountNoBackend')
            messages.success(request, 'Welcome, {}!'.format(user.full_name))
            return redirect("user_profile")

        return render(request, "accounts/login_form.html", {'form': form})

class ProfileView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "home/home.html")
        else:
            user = request.user
            return render(request, "accounts/account_info.html", {"user": user})

# From here Updating all the fields related to account details......................
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    success_message = 'User Updated Successfully!'
    fields = ['username', 'email', 'contact_no']
    success_url = '/'

class UserAccountUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AccountDetails
    success_message = f'Account Details Updated Successfully!'
    fields = [
        'branch_name',
        'account_type',
        'gender',
        'birth_date',
        'picture'
    ]
    success_url = '/'

class UserAddressUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserAddress
    success_message = 'User Address Updated Successfully!'
    fields = [
        'state',
        'district',
        'street_address',
        'postal_code',
    ]
    success_url = '/'