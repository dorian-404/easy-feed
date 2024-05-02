from django.shortcuts import render


# Create your views here.

def home_view(request):
    return render(request, 'html/home.html', context={})


def login_view(request):
    return render(request, 'html/login.html', context={})


def dashboard_view(request):
    return render(request, 'html/dashboard.html', context={})
