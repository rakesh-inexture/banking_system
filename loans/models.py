from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
class LoanDetails(models.Model):
    LOAN_TYPE_CHOICES = (
        ("HL", "Home Loan"),
        ("CL", "Car Loan"),
        ("PL", "Property Loan"),
        ("EL", "Education Loan"),
    )
    LOAN_DURATION_CHOICE = (
        ("1", "One Year"),
        ("2", "Two Years"),
        ("5", "Five Years"),
        ("10", "Ten Years")
    )
    LOAN_INTEREST_CHOICE = (
        ("5", "5%"),
        ("6", "6%"),
        ("7", "7%"),
        ("8", "8%")
    )
    user = models.ForeignKey(
        User,
        related_name='loans',
        on_delete=models.CASCADE,
    )
    loan_type = models.CharField(max_length=2, null=False, blank=False, choices=LOAN_TYPE_CHOICES)
    loan_duration = models.CharField(max_length=10, null=False, blank=False, choices=LOAN_DURATION_CHOICE)
    rate_of_interest = models.CharField(max_length=10, null=False, blank=False, choices=LOAN_INTEREST_CHOICE)
    loan_status = models.BooleanField(default=False)

    def __str__(self):
        return str(self.loan_type)