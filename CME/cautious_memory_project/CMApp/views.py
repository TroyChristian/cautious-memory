from django.shortcuts import render, HttpResponse, redirect
from . forms import EntryForm, CustomUserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        context = {}
        context["user"] = request.user
        return render(request, 'CMApp/dashboard.html', context)

    else:
        return render(request, 'CMApp/registration/login.html')


def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')

    else:
        f = CustomUserCreationForm()

    return render(request, 'CMApp/register.html', {'form': f})
