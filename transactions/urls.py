from django.urls import path
from .views import DepositView, WithdrawalView, WithdrawalOtpAuthView
from django.contrib.auth.decorators import login_required

app_name = 'transactions'
urlpatterns = [
    path('deposit/', login_required(DepositView.as_view()), name='deposit'),
    path('withdrawal/', login_required(WithdrawalView.as_view()), name='withdrawal'),
    path('otp_auth/', login_required(WithdrawalOtpAuthView.as_view()), name='otp_auth'),
]