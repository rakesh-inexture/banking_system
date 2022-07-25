from django.shortcuts import render, redirect
from django.views import View


class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "home/home.html")
        else:
            return redirect("user_profile")


class About(View):
    def get(self, request):
        return render(request, "home/about.html")
