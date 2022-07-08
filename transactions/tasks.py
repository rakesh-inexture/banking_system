from __future__ import absolute_import, unicode_literals
from celery import shared_task
from accounts.models import User
from .models import Interest, Deposit
from django.core.mail import send_mail
import random

@shared_task(name="count_interest")
def count():
    users = User.objects.filter(account__balance__isnull=False)
    # print("EXIT USER", users)
    if users.exists():
        for user in users:
            balance = user.balance
            # calculates users interest
            amount = (balance * 10) / 100
            Interest.objects.create(user=user, amount=amount)
            # adds users interest to balance.
            Deposit.objects.create(user=user, amount=amount)
            # adds interest amount in transaction history as well.
            user.account.balance += amount
            user.account.save()
@shared_task
def send_mail_task(user):
    email = user
    # print(email)
    send_otp = str(random.randint(1000, 9999))
    htmlgen = "<p>Your OTP for Authentication is <strong> {} </strong> </p>".format(send_otp)
    send_mail('OTP request', send_otp, 'rakeshkumar.18172@marwadieducation.edu.in', [email], fail_silently=False,
              html_message=htmlgen)
    # print(send_otp)
    return send_otp
