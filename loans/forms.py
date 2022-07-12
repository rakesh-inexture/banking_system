from django import forms
from .models import LoanDetails

class LoanApplyForm(forms.ModelForm):
    class Meta:
        model = LoanDetails
        fields = ['loan_duration', 'loan_type']