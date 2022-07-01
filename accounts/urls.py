from django.urls import path
from .views import RegisterView, LoginView, UserUpdateView, UserAccountUpdateView, UserAddressUpdateView, LoadDistricts, ProfileView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('user_profile', login_required(ProfileView.as_view()), name='user_profile'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home/home.html'), name='logout'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('account_update/<int:pk>/', UserAccountUpdateView.as_view(), name='account_update'),
    path('address_update/<int:pk>/', UserAddressUpdateView.as_view(), name='address_update'),
    path('ajax/load-districts/', LoadDistricts.as_view(), name='ajax_load_districts'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
