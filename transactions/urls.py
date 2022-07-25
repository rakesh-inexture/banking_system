from django.urls import path
from .views import DepositView, WithdrawalView, SendOtpView, CheckOtpView, TransactionsView, InterestView, \
    MoneyTransferView, AddPayeeView
from django.contrib.auth.decorators import login_required

app_name = 'transactions'
urlpatterns = [
    path('deposit/', login_required(DepositView.as_view()), name='deposit'),
    path('withdrawal/', login_required(WithdrawalView.as_view()), name='withdrawal'),
    path('send_otp/', login_required(SendOtpView.as_view()), name='send_otp'),
    path('check_otp/', login_required(CheckOtpView.as_view()), name='check_otp'),
    path('transaction_details/', login_required(TransactionsView.as_view()), name='transaction_details'),
    path('interest_details/', login_required(InterestView.as_view()), name='interest_details'),
    path('money_transfer', login_required(MoneyTransferView.as_view()), name='money_transfer'),
    path('add_payee', login_required(AddPayeeView.as_view()), name='add_payee')

]
