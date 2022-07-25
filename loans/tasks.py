from __future__ import absolute_import, unicode_literals
from celery import shared_task
from accounts.models import User
from loans.models import InterestRate
from transactions.models import Interest, Withdrawal


@shared_task(name="count_loan_interest")
def count():
    users = User.objects.filter(loan__loan_active_status=True)
    if users.exists():
        for user in users:
            if user.loan.loan_active_status:
                if user.loan.loan_tenure == 0:
                    user.account.balance -= user.loan.loan_amount
                    user.account.save()
                    user.loan.loan_active_status = False
                    user.loan.save()
                    Withdrawal.objects.create(user=user, amount=user.loan.loan_amount,
                                              status='Loan Amount debited')

                else:
                    amount = user.loan.loan_amount
                    interest = InterestRate.objects.get(id=user.loan.rate_of_interest_id)
                    rate_of_interest = interest.loan_interest
                    #  calculating loaner interest
                    amount = (amount * rate_of_interest) / 100
                    Withdrawal.objects.create(user=user, amount=amount, status='Loan Interest debited')
                    # adds interest amount in transaction history as well.
                    user.account.balance -= amount
                    user.account.save()
                    user.loan.loan_tenure -= 1
                    user.loan.save()
            else:
                pass
