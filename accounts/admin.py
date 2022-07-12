from django.contrib import admin
from .models import User, AccountDetails, UserAddress, State, District

@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    list_display = [
            "username",
            "full_name",
            "email",
            "contact_no",
        ]

@admin.register(AccountDetails)
class AccountModelAdmin(admin.ModelAdmin):
    list_display = [
            'account_type',
            'gender',
            'birth_date',
            'picture'
        ]

@admin.register(UserAddress)
class AddressModelAdmin(admin.ModelAdmin):
    list_display = [
            'state',
            'district',
            'street_address',
            'postal_code',
        ]

@admin.register(State)
class StateModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'state_name']

@admin.register(District)
class DistrictModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'district_name', 'state_id']

