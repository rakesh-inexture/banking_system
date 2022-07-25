from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from loans.models import LoanDetails
from accounts.models import AccountDetails


@receiver(post_save, sender=LoanDetails)
def update_loan_status(sender, instance, created, *args, **kwargs):
    if not created:
        loaner = LoanDetails.objects.get(user_id=instance.user_id)
        if loaner.loan_sanction_status:
            if not loaner.loan_credited_status:
                user_rcd = AccountDetails.objects.get(user_id=instance.user_id)
                user_rcd.balance += int(loaner.loan_amount)
                user_rcd.save()
                loaner.loan_credited_status = True
                loaner.loan_active_status = True
                loaner.save()
