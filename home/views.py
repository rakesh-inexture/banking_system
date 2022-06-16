from django.shortcuts import render

def home_view(request):
    if not request.user.is_authenticated:
        return render(request, "home/home.html")
    else:
        user = request.user

        context = {
            "user": user,
        }
        return render(request, "home/transactions.html", context)

def about(request):
    return render(request, "home/about.html", {})

