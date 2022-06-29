from django import forms
class DepositValid:
    def validate(self, amount):
        if amount < 10:
            raise forms.ValidationError('Please Enter Above 10Rs !!!')
    def get_help_text(self):
        return ('rakesh')

