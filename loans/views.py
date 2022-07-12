from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from accounts.models import AccountDetails
from .forms import LoanApplyForm
from .models import LoanDetails
from django.views import View

class ApplyLoan(View):
    def get(self, request):
        loan_form = LoanApplyForm()
        return render(request, 'loans/loan_apply.html', {'form': loan_form})
    def post(self, request):
        user = LoanDetails.objects.filter(user_id=request.user.id).exists()
        if user==False:
            loan_duration = request.POST.get('loan_duration')
            loan_type = request.POST.get('loan_type')
            if loan_type == 'HL':
                rate_of_interest = '8'
            elif loan_type == 'EL':
                rate_of_interest = '6'
            elif loan_type == 'CL':
                rate_of_interest = '9'
            elif loan_type == 'PL':
                rate_of_interest = '6'

            obj = LoanDetails(loan_type=loan_type, loan_duration=loan_duration, rate_of_interest=rate_of_interest, user_id=request.user.id)
            obj.save()
            messages.success(request, 'Successfully Applied for a loan')
            return redirect("user_profile")
        else:
            messages.error(request, 'Sorry! You have already Applied for a loan')
            return redirect("user_profile")

class LoanStatus(View):
    def get(self, request):
        user_rcd = LoanDetails.objects.get(user_id=request.user.id)
        if user_rcd.loan_status == True:
            messages.success(request, 'Congratulations, Your Loan has been approved by Bank! for further processs plz contact to Bank')
            return redirect("user_profile")
        else:
            messages.error(request, 'Sorry! You Loan status is pending till now.')
            return redirect("user_profile")


