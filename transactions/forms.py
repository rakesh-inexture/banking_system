from django import forms
from .models import Deposit, Withdrawal, PayeeDetails

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ["amount"]

class WithdrawalForm(forms.ModelForm):
    class Meta:
        model = Withdrawal
        fields = ["amount"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        # if kwargs has no key 'user', user is assigned None
        super(WithdrawalForm, self).__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.user.account.balance < amount:
            raise forms.ValidationError('You Can Not Withdraw More Than You Balance.')
        return amount
