from django.urls import path
from .views import ApplyLoan, LoanStatus
from django.contrib.auth.decorators import login_required

app_name = 'loans'
urlpatterns = [
    path('loan_form', login_required(ApplyLoan.as_view()), name='loan_form'),
    path('loan_status', login_required(LoanStatus.as_view()), name='loan_status'),

]