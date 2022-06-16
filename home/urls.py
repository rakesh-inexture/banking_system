from django.urls import path
from .views import home_view, about

app_name = 'home'

urlpatterns = [
    path('', home_view, name='home_view'),
    path('about/', about, name='about'),
]