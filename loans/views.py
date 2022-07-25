from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from .forms import LoanDurationForm
from .models import LoanDetails, InterestRate
from accounts.models import AccountDetails
from django.views import View


class ApplyLoan(View):
    def get(self, request):
        loan_duration = LoanDurationForm()
        loan_type = InterestRate.objects.all()
        return render(request, 'loans/loan_apply.html', {'loan_duration_form': loan_duration, 'loan_type': loan_type})

    def post(self, request):
        loaner = LoanDetails.objects.filter(user_id=request.user.id).exists()
        if not loaner:
            # if user not applied for loan till now then this part will be execute.
            loan_interest = InterestRate.objects.get(id=request.POST.get('loan_type_id'))
            loan_duration = int(request.POST.get('loan_duration'))
            loan_tenure = int(loan_duration) * 12
            loaner = LoanDetails.objects.create(loan_amount=request.POST.get('loan_amount'),
                                                loan_duration=loan_duration,
                                                rate_of_interest=loan_interest, user_id=request.user.id,
                                                loan_tenure=loan_tenure
                                                )
            loaner.save()
            messages.success(request, 'You Successfully Applied for a loan wait for approval')
            return render(request, "accounts/account_info.html", {'user': request.user})
        else:
            messages.warning(request, 'Sorry! You have already Applied for a loan')
            return redirect("user_profile")


class LoanStatus(View):
    def get(self, request):
        # print(request.POST)
        check_user = LoanDetails.objects.filter(user_id=request.user.id).exists()
        if check_user:
            loaner = LoanDetails.objects.get(user_id=request.user.id)
            if loaner.loan_credited_status:
                messages.info(request,
                              'Your Loan amount has been already credited to your account number')
                return redirect("user_profile")
            else:
                messages.info(request, 'Sorry! You Loan Application is pending.')
                return redirect("user_profile")
        else:
            messages.error(request, 'Sorry! You have not applied for loan.')
            return redirect("loans:loan_form")
