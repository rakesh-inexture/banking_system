from django import forms
from .models import LoanDetails, InterestRate

class LoanDurationForm(forms.ModelForm):
    class Meta:
        model = LoanDetails
        fields = ['loan_amount', 'loan_duration']
