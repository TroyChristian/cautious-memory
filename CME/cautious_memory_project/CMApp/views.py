from django.shortcuts import render, HttpResponse, redirect
from . forms import EntryForm, CustomUserCreationForm, AssetForm
from django.contrib import messages
from django.contrib.auth.models import User
from . models import Asset, Portfolio, Entry, Journal


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        context = {"user":request.user}

        return render(request, 'CMApp/dashboard.html', context)

    else:
        return render(request, 'CMApp/registration/login.html')

def add_asset(request):
    if request.method == "GET":
        # Show a forum where they can add an asset_value
        form = AssetForm()
        form.fields["owner_portfolio"].queryset = Portfolio.objects.filter(owner=request.user.id)
        context = {"asset_form":form}
        return render(request, 'CMApp/new_asset.html', context)

    if request.method == "POST":
        form = AssetForm(request.POST)
        form.owner_portfolio = request.user.username
        #print(form.owner_portfolio.owner.id)
        if form.is_valid():
            form.save()

        context = {"user":request.user}
        return render(request, 'CMApp/dashboard.html', context)
    #initial = {"owner_portfolio": request.user.user_portfolio}
    #form = AssetForm(initial=initial)

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
