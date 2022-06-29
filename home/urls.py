from django.urls import path
from .views import HomeView, About

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home_view'),
    path('about/', About.as_view(), name='about'),

]