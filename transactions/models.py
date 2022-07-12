from django.db import models
from decimal import Decimal
from django.conf import settings
from django.core.validators import MinValueValidator

User = settings.AUTH_USER_MODEL
class Deposit(models.Model):
    user = models.ForeignKey(
        User,
        related_name='deposits',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(default="credited", max_length=10)

    def __str__(self):
        return f"{str(self.user)}: {self.amount}"


class Withdrawal(models.Model):
    user = models.ForeignKey(
        User,
        related_name='withdrawals',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        validators=[
            MinValueValidator(Decimal('10.00'))
        ]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    status = models.CharField(default="debited", max_length=10)

    def __str__(self):
        return f"{str(self.user)}: {self.amount}"


class WithdrawalOtp(models.Model):
    user = models.ForeignKey(
        User,
        related_name='otpauth',
        on_delete=models.CASCADE,
    )
    otp = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{str(self.user)}: {self.otp}"


class Interest(models.Model):
    user = models.ForeignKey(
        User,
        related_name='interests',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)


class PayeeDetails(models.Model):
    user = models.ForeignKey(
        User,
        related_name='payee',
        on_delete=models.CASCADE,
    )
    payee_account = models.CharField(max_length=20)
    payee_ifsc = models.CharField(max_length=30)

    def __str__(self):
        return self.payee_account
