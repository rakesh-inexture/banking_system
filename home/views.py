from django.shortcuts import render
from django.views import View
from accounts.models import AccountDetails

class HomeView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, "home/home.html")
        else:
            profile = AccountDetails.objects.get(user_id=request.user.id)
            print(profile)
            return render(request, "home/transactions.html", {"profile": profile})

class About(View):
    def get(self, request):
        return render(request, "home/about.html", {})

