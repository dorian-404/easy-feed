from django.shortcuts import render


# Create your views here.

def home(request):
    return render(request, 'html/home.html', context={})


def login(request):
    return render(request, 'html/login.html', context={})


def dashboard(request):
    return render(request, 'html/dashboard.html', context={})
