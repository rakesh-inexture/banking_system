from django.contrib import admin
from .models import LoanDetails

@admin.register(LoanDetails)
class LoanDetailsAdmin(admin.ModelAdmin):
    list_display = [
            "loan_type",
            "loan_duration",
            "rate_of_interest",
            "loan_status",
            "user"
        ]
