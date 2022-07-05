from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from .forms import DepositForm, WithdrawalForm
from .models import WithdrawalOtp
# from .helpers import sendOtp
from .tasks import send_mail_task
from django.db.models import Sum
from itertools import chain
from transactions.models import Deposit, Withdrawal, Interest

class DepositView(View):
    def get(self, request):
        form = DepositForm()
        return render(request, "transactions/deposit_form.html", {"form": form})

    def post(self, request):
        form = DepositForm(request.POST or None)
        # print(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            # print(request.user)
            deposit.save()
            # adds users deposit to balance.
            deposit.user.account.balance += deposit.amount
            deposit.user.account.save()
            messages.success(request, 'You Have Deposited ₹ {}.'.format(deposit.amount))
            return redirect("user_profile")
        return render(request, 'transactions/deposit_form.html', {'form': form})

class WithdrawalView(View):
    def get(self, request):
        form = WithdrawalForm()
        # print("GET REQ", request.user)
        return render(request, "transactions/withdraw_form.html", {"form": form})

class SendOtpView(View):
    def post(self, request):
        # form = WithdrawalForm(request.POST or None, user=request.user)
        # send_otp = sendOtp(request.user)
        send_otp = send_mail_task(request.user)
        # # print("REQ", request)
        # print("OTP", send_otp)
        # # print("USER", request.user)
        # print("AMOUNT", request.POST.get('amount'))
        # print(form.is_valid())
        # if form.is_valid():
        user_id = request.POST.get('user_id')
        otp_obj, created = WithdrawalOtp.objects.get_or_create(user_id=user_id)
        otp_obj.otp = send_otp
        otp_obj.save()
        return HttpResponse('success')

class WithdrawalOtpAuthView(View):
    def post(self, request):
        form = WithdrawalForm(request.POST or None, user=request.user)
        # print(dir(request))
        # print("REQ_POST", request.POST)
        # print("USER", request.user)
        # print("USER_ID", request.user.id)
        send_otp = WithdrawalOtp.objects.filter(user_id=request.user.id)
        # print("SEND_OTP", send_otp[0].otp)
        # print("SEND_OTP", dir(send_otp))
        # print("USER_OTP", request.POST.get('otp'))
        if send_otp[0].otp == int(request.POST.get('otp')):
            if form.is_valid():
                withdrawal = form.save(commit=False)
                withdrawal.user = request.user
                withdrawal.save()
                # subtracting users withdrawal from balance.
                withdrawal.user.account.balance -= withdrawal.amount
                withdrawal.user.account.save()
                messages.success(
                    request, 'You Have Withdrawn ₹ {}.'.format(withdrawal.amount)
                )
                return redirect("user_profile")

            return render(request, 'transactions/withdraw_form.html', {'form': form})

        messages.error(request, 'Sorry! Your OTP is not Matching with Send OTP on Email! Try Again!')
        return redirect("user_profile")

class TransactionsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "home/home.html")
        else:
            user = request.user
            deposit_list = Deposit.objects.filter(user=user)
            deposit_sum = deposit_list.aggregate(Sum('amount'))['amount__sum']
            withdrawal_list = Withdrawal.objects.filter(user=user)
            withdrawal_sum = withdrawal_list.aggregate(Sum('amount'))['amount__sum']
            transaction_list = sorted(chain(deposit_list, withdrawal_list), key=lambda instance: instance.timestamp)
            paginator = Paginator(transaction_list, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                "user": user,
                "deposit_sum": deposit_sum,
                "withdrawal_sum": withdrawal_sum,
                "page_obj": page_obj
            }
            return render(request, "transactions/account_transaction.html", context)

class InterestView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "home/home.html")
        else:
            user = request.user
            interest = Interest.objects.filter(user=user)
            interest_sum = interest.aggregate(Sum('amount'))['amount__sum']
            context = {
                "user": user,
                "interest": interest,
                "interest_sum": interest_sum,
            }
            return render(request, "transactions/account_interest.html", context)

