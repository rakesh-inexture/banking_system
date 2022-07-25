import datetime
from django.db import models
from accounts.models import User


class InterestRate(models.Model):
    loan_type = models.CharField(max_length=50, null=False, blank=False)
    loan_interest = models.IntegerField()

    def __str__(self):
        return self.loan_type


class LoanDetails(models.Model):
    LOAN_DURATION_CHOICE = (
        (1, "One Year"),
        (2, "Two Years"),
        (3, "Three Years"),
        (4, "Four Years"),
        (5, "Five Years")
    )
    user = models.OneToOneField(User, related_name='loan', on_delete=models.CASCADE)
    rate_of_interest = models.ForeignKey(InterestRate, related_name='loans_loan_interest', on_delete=models.CASCADE)
    loan_duration = models.IntegerField(choices=LOAN_DURATION_CHOICE)
    loan_amount = models.DecimalField(max_digits=12, decimal_places=2)
    loan_sanction_status = models.BooleanField(default=False)
    loan_credited_status = models.BooleanField(default=False)
    loan_active_status = models.BooleanField(default=False)
    loan_tenure = models.IntegerField()
    loan_applied_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.user.email
