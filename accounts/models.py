from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
# from secrets import SystemRandom


class User(AbstractUser):
    username = models.CharField(max_length=50)

    email = models.EmailField(unique=True, null=False, blank=False)
    contact_no = models.CharField(max_length=12, unique=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    # It is a built-in decorator it  help in defining the properties effortlessly without manually calling the inbuilt function property().
    # It return the property attributes of a class from the stated getter, setter and deleter as parameters.

    def account_no(self):
        if hasattr(self, 'account'):
            # here hasattr() checking for the existence of an attribute, if TRUE then returning it.
            return self.account.account_no
        return None

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    @property
    def balance(self):
        if hasattr(self, 'account'):
            return self.account.balance
        return None

    @property
    def full_address(self):
        if hasattr(self, 'address'):
            return '{}, {}-{}, {}'.format(
                self.address.street_address,
                self.address.city,
                self.address.postal_code,
                self.address.country,
            )
        return None

class AccountDetails(models.Model):
    GENDER_CHOICE = (
        ("M", "Male"),
        ("F", "Female"),
    )
    ACCOUNT_CHOICE = (
        ("C", "Current"),
        ("S", "Saving"),
    )
    BRANCH_CHOICE = (
        ("SHI", "Shivranjani"),
        ("ISK", "Iskon"),
        ("SCI", "Science City")
    )
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.PositiveIntegerField(
        unique=True,
        validators=[
            MinValueValidator(10000000),
            MaxValueValidator(99999999)
        ]
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    branch_name = models.CharField(max_length=3, choices=BRANCH_CHOICE)
    account_type = models.CharField(max_length=1, null=False, blank=False, choices=ACCOUNT_CHOICE)
    birth_date = models.DateField(null=True, blank=True, help_text="Date format must be YYYY-MM-DD")
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    picture = models.ImageField(
        null=True,
        blank=True,
        upload_to='account_pictures/',
    )

    def __str__(self):
        return str(self.account_no)


class UserAddress(models.Model):
    user = models.OneToOneField(
        User,
        related_name='address',
        on_delete=models.CASCADE,
    )
    street_address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    postal_code = models.CharField(max_length=6)
    country = models.CharField(max_length=256)

    def __str__(self):
        return self.user.email

