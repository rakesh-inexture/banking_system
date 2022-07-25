import datetime
import pytest
from django.urls import reverse
# from django.contrib.auth.models import User
from loans.models import *
from django.test.client import Client
from transactions.models import *
from accounts.models import *


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def admin_user_data():
    ad_user = User.objects.create_user(
        username="Rk",
        email='rk@gmail.com',
        password="rk@12345"
    )
    ad_user.save()
    return ad_user


@pytest.fixture
def user():
    new_user = User.objects.create_user(
        username='rakesh@123',
        first_name='Rakesh',
        last_name='kumar',
        email='rakesh0506907@gmail.com',
        contact_no='9097142242',
        password='kr@12345',
    )
    new_user.set_password('kr@12345')
    new_user.save()
    return new_user


@pytest.fixture
def account_data(user):
    ac_data = AccountDetails.objects.create(
        user=user,
        gender='M',
        account_no=10000003,
        account_type='S',
        birth_date='1999-10-15',
        ifsc_code='RK012345',
        balance=5000
    )
    ac_data.save()
    return ac_data


@pytest.fixture
def state_data():
    st_data = State.objects.create(
        state_name='Gujarat',
    )
    st_data.save()
    return st_data


@pytest.fixture
def district_data(state_data):
    dist_data = District.objects.create(
        state=state_data,
        district_name='Ahmedabad'
    )
    dist_data.save()
    return dist_data


@pytest.fixture
def branch_data(district_data):
    bran_data = Branch.objects.create(
        district=district_data,
        branch_name='Iskcon',
    )
    bran_data.save()
    return bran_data


@pytest.fixture
def address_data(user, account_data, state_data, district_data, branch_data):
    addr_data = AddressDetails.objects.create(
        user=user,
        street_address='Shivranjani',
        postal_code='380015',
        branch_name=branch_data,
        district=district_data,
        state=state_data,
    )
    addr_data.save()
    # print(f"ADDRESS {addr_data}")
    return addr_data


@pytest.fixture
def login_user(client, account_data, user):
    url = reverse('login')
    response = client.post(url, dict(account_no=account_data.account_no, password='kr@12345'))
    # print(f"LOGIN{response}")
    return response


@pytest.fixture
def loan_interest():
    loan_int = InterestRate.objects.create(
        loan_type='Home Loan',
        loan_interest=8
    )
    loan_int.save()
    return loan_int


@pytest.fixture
def loan_details(user, loan_interest):
    loan_det = LoanDetails.objects.create(
        user=user,
        rate_of_interest=loan_interest,
        loan_duration='1',
        loan_amount=1500.00,
        loan_status=False,
        loan_amount_credited_status=False,
        loan_applied_date=datetime.datetime.now(),
    )
    loan_det.save()
    return loan_det


@pytest.fixture
def withdrawal_otp_data(user):
    otp_data = WithdrawalOtp.objects.create(
        user=user,
        otp=9337
    )
    otp_data.save()
    return otp_data


@pytest.fixture
def payee_details_data(user, account_data):
    otp_data = PayeeDetails.objects.create(
        payee_account=account_data.account_no,
        payee_ifsc=account_data.ifsc_code,
        user=user
    )
    otp_data.save()
    return otp_data
