import pytest
from django.urls import reverse, resolve
from accounts.views import *
from home.views import *
from loans.views import *
from transactions.views import *
from django.contrib.auth import views as auth_views


def test_register_url():
    url = reverse('register')
    assert resolve(url).func.view_class == RegisterView


def test_login_url():
    url = reverse('login')
    assert resolve(url).func.view_class == LoginView


def test_user_profile_url():
    url = reverse('user_profile')
    assert resolve(url).func.view_class == ProfileView


def test_logout_url():
    url = reverse('logout')
    assert resolve(url).func.view_class == auth_views.LogoutView


def test_user_update_url():
    url = reverse('user_update', args=[1])
    assert resolve(url).func.view_class == UserUpdateView


def test_account_update_url():
    url = reverse('account_update', args=[1])
    assert resolve(url).func.view_class == UserAccountUpdateView


def test_address_update_url():
    url = reverse('address_update', args=[1])
    assert resolve(url).func.view_class == UserAddressUpdateView


def test_load_district_url():
    url = reverse('load_districts')
    assert resolve(url).func.view_class == LoadDistrictsView


def test_load_branches_url():
    url = reverse('load_branches')
    assert resolve(url).func.view_class == LoadBranchView


def test_password_reset_url():
    url = reverse('password_reset')
    assert resolve(url).func.view_class == auth_views.PasswordResetView


def test_password_reset_done_url():
    url = reverse('password_reset_done')
    assert resolve(url).func.view_class == auth_views.PasswordResetDoneView


# def test_password_reset_confirm_url():
#     url = reverse('password_reset_confirm')
#     assert resolve(url).func.view_class == auth_views.PasswordResetCompleteView


def test_password_reset_complete_url():
    url = reverse('password_reset_complete')
    assert resolve(url).func.view_class == auth_views.PasswordResetCompleteView


def test_home_url():
    url = reverse('home:home_view')
    assert resolve(url).func.view_class == HomeView


def test_about_url():
    url = reverse('home:about')
    assert resolve(url).func.view_class == About


def test_loan_applied_url():
    url = reverse('loans:loan_form')
    assert resolve(url).func.view_class == ApplyLoan


def test_loan_status_url():
    url = reverse('loans:loan_status')
    assert resolve(url).func.view_class == LoanStatus


def test_deposit_url():
    url = reverse('transactions:deposit')
    assert resolve(url).func.view_class == DepositView


def test_withdrawal_url():
    url = reverse('transactions:withdrawal')
    assert resolve(url).func.view_class == WithdrawalView


def test_send_otp_url():
    url = reverse('transactions:send_otp')
    assert resolve(url).func.view_class == SendOtpView


def test_check_otp_url():
    url = reverse('transactions:check_otp')
    assert resolve(url).func.view_class == CheckOtpView


def test_transactions_details_url():
    url = reverse('transactions:transaction_details')
    assert resolve(url).func.view_class == TransactionsView


def test_interest_details_url():
    url = reverse('transactions:interest_details')
    assert resolve(url).func.view_class == InterestView


def test_money_transfer_url():
    url = reverse('transactions:money_transfer')
    assert resolve(url).func.view_class == MoneyTransferView


def test_add_payee_url():
    url = reverse('transactions:add_payee')
    assert resolve(url).func.view_class == AddPayeeView
