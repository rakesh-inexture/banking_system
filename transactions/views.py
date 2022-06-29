from django.contrib import messages
# from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .forms import DepositForm, WithdrawalForm, OtpForm
from .models import WithdrawalOtp
from .utils import sendOtp
from django.shortcuts import render
# from django.views import View

class DepositView(View):
    def get(self, request):
        form = DepositForm()
        return render(request, "transactions/deposit_form.html", {"form": form})

    def post(self, request):
        form = DepositForm(request.POST or None)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            # print(request.user)
            deposit.save()
            # adds users deposit to balance.
            deposit.user.account.balance += deposit.amount
            deposit.user.account.save()
            messages.success(request, 'You Have Deposited ₹ {}.'.format(deposit.amount))
            return redirect("home:home_view")

        return render(request, 'transactions/deposit_form.html', {'form': form})

class WithdrawalView(View):
    def get(self, request):
        form = WithdrawalForm()
        return render(request, "transactions/withdraw_form.html", {"form": form})
        # print(request.user)

    def post(self, request):
        # print(request.POST)
        form = WithdrawalForm(request.POST or None, user=request.user)
        if form.is_valid():
            # print("POST Requesting", request.POST)
            # sendotp=sendOtp(request.user)
            # otpform= OtpForm()
            # return render(request, "transactions/verify_otp_form.html", {"form": otpform})
            # # if otp_auth(request.user)==True:
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            withdrawal.save()
            # subtracting users withdrawal from balance.
            withdrawal.user.account.balance -= withdrawal.amount
            withdrawal.user.account.save()
            messages.success(
                request, 'You Have Withdrawn ₹ {}.'.format(withdrawal.amount)
            )
            return redirect("home:home_view")

        return render(request, 'transactions/withdraw_form.html', {'form': form})

class WithdrawalOtpAuthView(View):
    def get(self, request):
        send_otp = sendOtp(request.user)
        user = request.user
        otp_obj, created = WithdrawalOtp.objects.get_or_create(user=user)
        otp_obj.otp = send_otp
        otp_obj.save()

        otp_form = OtpForm()
        return render(request, "transactions/verify_otp_form.html", {"otp_form": otp_form})

    def post(self, request):
        otp_form = OtpForm(request.POST)
        if otp_form.is_valid():
            otp = WithdrawalOtp.objects.get(user_id=request.user.user_id)
            if otp == request.otp:
                return JsonResponse({"status": True})
            else:
                return JsonResponse({"status": False})
        else:
            return JsonResponse({"status": False})
