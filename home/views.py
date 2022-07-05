from django.shortcuts import render, redirect
from django.views import View
from accounts.models import AccountDetails

class HomeView(View):
    def get(self, request):
        return render(request, "home/home.html", {})

class About(View):
    def get(self, request):
        return render(request, "home/about.html", {})
