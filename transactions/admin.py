from django.contrib import admin
from .models import Deposit, Withdrawal, WithdrawalOtp, Interest

@admin.register(Deposit)
class DepositModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'timestamp', 'user']

@admin.register(Withdrawal)
class WithdrawalModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'timestamp', 'user']

@admin.register(WithdrawalOtp)
class WithrawalOtpModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'otp']

@admin.register(Interest)
class InterestModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'amount', 'timestamp', 'user']


