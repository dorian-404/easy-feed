from django.shortcuts import render


# Create your views here.

def index(request):
    return render(request, 'html/home.html', context={})


def home(request):
    return render(request, 'html/login.html', context={})