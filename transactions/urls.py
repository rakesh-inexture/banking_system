from django.urls import path
from .views import DepositView, WithdrawalView, WithdrawalOtpAuthView, SendOtpView, TransactionsView, InterestView
from django.contrib.auth.decorators import login_required

app_name = 'transactions'
urlpatterns = [
    path('deposit/', login_required(DepositView.as_view()), name='deposit'),
    path('withdrawal/', login_required(WithdrawalView.as_view()), name='withdrawal'),
    path('send_otp/', login_required(SendOtpView.as_view()), name='send_otp'),
    path('otp_auth/', login_required(WithdrawalOtpAuthView.as_view()), name='otp_auth'),
    path('transaction_details/', login_required(TransactionsView.as_view()), name='transaction_details'),
    path('interest_details/', login_required(InterestView.as_view()), name='interest_details'),

]