from django.db.models import Max
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import AccountDetails


@receiver(pre_save, sender=AccountDetails)
# pre_save-> This is sent at the beginning of a model's save() method.
def create_account_no(sender, instance, *args, **kwargs):
    # checks if user has an account number and user is not staff or superuser
    if not instance.account_no and not (instance.user.is_staff or instance.user.is_superuser):
        # gets the largest account number
        largest = AccountDetails.objects.aggregate(Max("account_no"))['account_no__max']
        # if there will no any account found then it will return None:->{'account_no__max': None}
        if largest:
            # creates new account number
            instance.account_no = largest + 1
        else:
            # if there is no other user, sets users account number to 10000000.
            instance.account_no = 10000000
