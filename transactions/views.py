from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from .forms import DepositForm, WithdrawalForm
from .models import WithdrawalOtp, PayeeDetails
from accounts.models import AccountDetails, User
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
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.save()
            deposit.user.account.balance += deposit.amount
            deposit.user.account.save()
            messages.success(request, 'You Have Deposited ₹ {}.'.format(deposit.amount))
            return redirect("user_profile")
        return render(request, 'transactions/deposit_form.html', {'form': form})


class WithdrawalView(View):
    def get(self, request):
        form = WithdrawalForm()
        return render(request, "transactions/withdraw_form.html", {"form": form})

    def post(self, request):
        form = WithdrawalForm(request.POST or None, user=request.user)
        if form.is_valid():
            withdrawal = form.save(commit=False)
            withdrawal.user = request.user
            withdrawal.save()
            # subtracting users withdrawal from balance.
            withdrawal.user.account.balance -= withdrawal.amount
            withdrawal.user.account.save()
            messages.success(request, 'You Have Withdrawn ₹ {}.'.format(withdrawal.amount))
            return redirect("user_profile")
        else:
            return render(request, 'transactions/withdraw_form.html', {'form': form})


class SendOtpView(View):
    def get(self, request):
        send_otp = send_mail_task(request.user)
        otp_obj, created = WithdrawalOtp.objects.get_or_create(user_id=request.user.id)
        otp_obj.otp = send_otp
        ack = otp_obj.save()
        if ack is None:
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 0})


class CheckOtpView(View):
    def get(self, request):
        send_otp = WithdrawalOtp.objects.filter(user_id=request.user.id)
        if send_otp[0].otp == int(request.GET.get('otp')):
            return JsonResponse({'status': 1})
        else:
            return JsonResponse({'status': 0})


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
            interest_list = Interest.objects.filter(user=user)
            interest_sum = interest_list.aggregate(Sum('amount'))['amount__sum']
            # interest_list = sorted(interest_list)
            paginator = Paginator(interest_list, 5)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            context = {
                "user": user,
                "interest_sum": interest_sum,
                "page_obj": page_obj
            }
            return render(request, "transactions/account_interest.html", context)


class MoneyTransferView(View):
    def get(self, request):
        try:
            payee_list = PayeeDetails.objects.all().exclude(payee_account=request.user.account.account_no)
        except PayeeDetails.DoestNotExist:
            payee_list = None
        finally:
            return render(request, 'money_transfer/money_transfer_form.html', {'payee_list': payee_list})

    def post(self, request):
        print(f"REQUEST{request.POST}")
        payee_details = PayeeDetails.objects.get(id=request.POST.get('payee_id'))
        # from Selected payee_id, i got payee's bank account.
        payee = AccountDetails.objects.get(account_no=payee_details.payee_account)
        # from payee's bank account i got his/her balance by obj payee obj
        payer = AccountDetails.objects.get(account_no=request.user.account.account_no)
        # Creating Payer obj for manipulation balance. like subtract amt..
        if request.POST.get('mode') == '1':
            users = User.objects.filter(account__balance__isnull=False)
            # mode 1 is IMPS and mode 2 is NEFT
            send_amt = float(request.POST.get('send_amt'))
            if float(send_amt + send_amt * 0.10) <= float(payer.balance):
                payer.balance -= int(
                    float(request.POST.get('send_amt')) + float(float(request.POST.get('send_amt')) * 0.10))
                payer.save()
                payee.balance += int(request.POST.get('send_amt'))
                payee.save()
                payer_withdrawal = Withdrawal(amount=send_amt, user_id=request.user.id)
                payer_withdrawal.save()
                payee_withdrawal = Deposit(amount=send_amt, user_id=payee_details.user_id)
                payee_withdrawal.save()
                messages.success(request,
                                 f'Amount ₹ {send_amt} Successfully transferred to Account no {payee_details.payee_account}')
                return redirect("user_profile")
            else:
                messages.error(request, 'Sorry, Your Account have not sufficient balance to transfer of this amount')
                return redirect("user_profile")

        elif request.POST.get('mode') == '2':
            send_amt = float(request.POST.get('send_amt'))

            if float(send_amt + send_amt * 0.05) <= float(payer.balance):
                payer.balance -= int(
                    float(request.POST.get('send_amt')) + float(float(request.POST.get('send_amt')) * 0.05))
                payer.save()
                payee.balance += int(request.POST.get('send_amt'))
                payee.save()
                payer_withdrawal = Withdrawal(amount=send_amt, user_id=request.user.id)
                payer_withdrawal.save()
                payee_withdrawal = Deposit(amount=send_amt, user_id=payee_details.user_id)
                payee_withdrawal.save()
                messages.success(request,
                                 f'Amount ₹ {send_amt} Successfully transferred to Account no {payee_details.payee_account} ')
                return redirect("user_profile")
            else:
                messages.error(request, 'Sorry, Your Account have not sufficient balance to transfer of this amount')
                return redirect("user_profile")


class AddPayeeView(View):
    def get(self, request):
        payee_ac = PayeeDetails.objects.values('payee_account')
        account_list = AccountDetails.objects.values('id', 'account_no', 'ifsc_code')
        for payee in payee_ac:
            account = int(payee['payee_account'])
            account_list = account_list.exclude(account_no=account)
        account_list = account_list.exclude(account_no=request.user.account.account_no)
        return render(request, 'money_transfer/add_payee_form.html', {'account_list': account_list})

    def post(self, request):
        user_id = int(request.POST.get('ac_id'))
        ad = AccountDetails.objects.get(id=user_id)
        account_no = ad.account_no
        ifsc = ad.ifsc_code
        PayeeDetails(payee_account=account_no, payee_ifsc=ifsc, user_id=ad.user_id).save()
        messages.success(request, 'Payee details added successfully!')
        return redirect('user_profile')
