import pytest


@pytest.mark.django_db
def test_user_model(user):
    assert user.username == "rakesh@123"
    assert user.email == "rakesh0506907@gmail.com"
    assert user.contact_no == '9097142242'


@pytest.mark.django_db
def test_account_details_model(account_data):
    assert account_data.gender == "M"
    assert account_data.account_type == "S"
    assert account_data.account_no == 10000003


@pytest.mark.django_db
def test_state_model(state_data):
    assert state_data.state_name == 'Gujarat'


@pytest.mark.django_db
def test_district_model(district_data, state_data):
    assert district_data.state == state_data
    assert district_data.district_name == 'Ahmedabad'


@pytest.mark.django_db
def test_branch_model(branch_data, district_data):
    assert branch_data.district == district_data
    assert branch_data.branch_name == 'Iskcon'


@pytest.mark.django_db
def test_address_details_model(address_data, branch_data, district_data, state_data):
    assert address_data.street_address == 'Shivranjani'
    assert address_data.postal_code == '380015'
    assert address_data.branch_name == branch_data
    assert address_data.district == district_data
    assert address_data.state == state_data


@pytest.mark.django_db
def test_loan_interest_model(loan_interest):
    assert loan_interest.loan_type == 'Home Loan'
    assert loan_interest.loan_interest == 8


@pytest.mark.django_db
def test_loan_details_model(loan_details, user, loan_interest):
    assert loan_details.user == user
    assert loan_details.rate_of_interest == loan_interest
    assert loan_details.loan_duration == '1'
    assert loan_details.loan_status == False
    assert loan_details.loan_amount_credited_status == False


@pytest.mark.django_db
def test_payee_details_model(payee_details_data, account_data, user):
    assert payee_details_data.payee_account == account_data.account_no
    assert payee_details_data.payee_ifsc == account_data.ifsc_code
    assert payee_details_data.user == user


@pytest.mark.django_db
def test_withdrawal_otp_model(withdrawal_otp_data, user):
    assert withdrawal_otp_data.user == user
    assert withdrawal_otp_data.otp == 9337
