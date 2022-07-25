import pytest
from django.urls import reverse
# from accounts.models import User
from loans.models import *


@pytest.mark.django_db
def test_create_admin_user(admin_user_data):
    count = User.objects.all().count()
    print("COUNT", count)
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_register_get(client):
    url = reverse('register')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_register_post(client, user, account_data, address_data):
    register_data = {
        'username': 'shyam@123',
        'first_name': 'Shyam',
        'last_name': 'Kumar',
        'email': 'rakesh0506907@hotmail.com',
        'contact_no': '7004921821',
        'password1': 'rk@12345',
        'password2': 'rk@12345',
        'street_address': address_data.street_address,
        'postal_code': address_data.postal_code,
        'state': address_data.state.id,
        'district': address_data.district.id,
        'branch_name': address_data.branch_name.id,
        'account_type': account_data.account_type,
        'gender': account_data.gender,
        'birth_date': account_data.birth_date,
        'picture': ''
    }
    url = reverse('register')
    response = client.post(url, data=register_data)
    # print(f"REGISTER{response.content}")
    assert response.status_code == 302


@pytest.mark.django_db
def test_login_get(client):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_post(client):
    url = reverse('login')
    response = client.post(url, {'account_no': 10000000, 'password': 'abc@12345'})
    # print(f"LOGIN{response}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_load_district(client):
    url = reverse('load_districts')
    response = client.get(url, args=[1])
    assert response.status_code == 200


@pytest.mark.django_db
def test_load_branch(client):
    url = reverse('load_branches')
    response = client.get(url, {'district_id': 1})
    assert response.status_code == 200


@pytest.mark.django_db
def test_load_branch(client):
    url = reverse('load_branches')
    response = client.get(url, {'district_id': 1})
    assert response.status_code == 200


def test_home_view(client):
    url = reverse('home:home_view')
    response = client.get(url)
    assert 'Developed by RAKESH KUMAR.' in str(response.content)
    assert response.status_code == 200


def test_home_about(client):
    url = reverse('home:about')
    response = client.get(url)
    assert 'It is fully designed by using Django framework of python' in str(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_loan_applied_get(client, login_user):
    url = reverse('loans:loan_form')
    response = client.get(url)
    print(f"TEST{response}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_loan_applied_post(client, login_user, loan_interest):
    data = {
        'loan_type_id': loan_interest.id,
        'loan_duration': '1',
        'loan_amount': 1500.0
    }
    url = reverse('loans:loan_form')
    response = client.post(url, data=data)
    print(f"TEST{response}")
    assert response.status_code == 200


@pytest.mark.django_db
def test_loan_status(client, login_user, loan_details):
    url = reverse('loans:loan_status')
    response = client.get(url)
    print(f"LOAN STATUS{response}")
    assert response.status_code == 302
    print(f"BANK NAME{response.content}")
    # assert "RK Bank" in str(response.content)


@pytest.mark.django_db
def test_deposit_get(client, login_user):
    url = reverse('transactions:deposit')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_deposit_post(client, login_user):
    data = {
        'amount': 200,
    }
    url = reverse('transactions:deposit')
    response = client.post(url, data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_withdrawal_get(client, login_user):
    url = reverse('transactions:withdrawal')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_withdrawal_post(client, login_user):
    data = {
        'amount': 400
    }
    url = reverse('transactions:withdrawal')
    response = client.post(url, data=data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_withdrawal_post_amount_not_valid(client, login_user):
    data = {
        'amount': 5
    }
    url = reverse('transactions:withdrawal')
    response = client.post(url, data=data)
    assert response.status_code == 200



@pytest.mark.django_db
def test_send_otp(client, login_user):
    url = reverse('transactions:send_otp')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_check_otp(client, login_user, withdrawal_otp_data):
    data = {
        'otp': withdrawal_otp_data.otp
    }
    url = reverse('transactions:check_otp')
    response = client.get(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_transactions(client, login_user):
    url = reverse('transactions:transaction_details')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_interest_transactions(client, login_user):
    url = reverse('transactions:interest_details')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_money_transfer_get(client, login_user):
    url = reverse('transactions:money_transfer')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_money_transfer_imps_post(client, login_user, withdrawal_otp_data, payee_details_data):
    data = {
        'payee_id': payee_details_data.id,
        'mode': 1,
        'send_amt': 500,
        'otp': withdrawal_otp_data.otp
    }
    url = reverse('transactions:money_transfer')
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_money_transfer_neft_post(client, login_user, withdrawal_otp_data, payee_details_data):
    data = {
        'payee_id': payee_details_data.id,
        'mode': 2,
        'send_amt': 500,
        'otp': withdrawal_otp_data.otp
    }
    url = reverse('transactions:money_transfer')
    response = client.post(url, data)
    assert response.status_code == 302


@pytest.mark.django_db
def test_add_payee_get(client, login_user):
    url = reverse('transactions:add_payee')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_payee_post(client, login_user, account_data):
    data = {
        'ac_id': account_data.id
    }
    url = reverse('transactions:add_payee')
    response = client.post(url, data=data)
    assert response.status_code == 302
