from django.contrib import admin
from .models import LoanDetails, InterestRate


@admin.register(InterestRate)
class InterestRateAdmin(admin.ModelAdmin):
    list_display = [
        "loan_type",
        "loan_interest"
    ]


@admin.register(LoanDetails)
class LoanDetailsAdmin(admin.ModelAdmin):
    list_display = [
        "loan_duration",
        "rate_of_interest",
        "loan_sanction_status",
        "loan_credited_status",
        "loan_active_status",
        "user"
    ]
