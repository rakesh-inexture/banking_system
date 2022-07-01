from django.urls import path
from .views import DepositView, WithdrawalView, WithdrawalOtpAuthView, SendOtpView
from django.contrib.auth.decorators import login_required

app_name = 'transactions'
urlpatterns = [
    path('deposit/', login_required(DepositView.as_view()), name='deposit'),
    path('withdrawal/', login_required(WithdrawalView.as_view()), name='withdrawal'),
    path('send_otp/', login_required(SendOtpView.as_view()), name='send_otp'),
    path('otp_auth/', login_required(WithdrawalOtpAuthView.as_view()), name='otp_auth'),
]