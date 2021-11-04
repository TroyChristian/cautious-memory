from django.shortcuts import render, HttpResponse, redirect
from . forms import EntryForm, CustomUserCreationForm, AssetForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import Asset, Portfolio, Entry, Journal


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        # Fetch a users asset
        user_assets = Asset.objects.filter(owner_portfolio = request.user.id)
        context = {"user":request.user,
                    "assets":user_assets,

                    }

        return render(request, 'CMApp/dashboard.html', context)

    else:
        return render(request, 'CMApp/registration/login.html')

def new_entry(request, asset):
    if request.method == "GET":
        form = EntryForm()
        user_portfolio_qs = Portfolio.objects.filter(owner=request.user.id)
        portfolio = user_portfolio_qs[0]
        assets = Asset.objects.filter(owner_portfolio=portfolio)
        current_asset_qs = assets.filter(ticker=asset)
        current_asset = current_asset_qs[0]
        print(current_asset)


        #asset_journal_qs = Journal.objects.filter(tracked_asset = asset.journal)
        form.fields["journal"].queryset = Journal.objects.filter(tracked_asset = current_asset.id)
        return render(request, 'CMApp/new_entry.html', {"entry_form":form, "asset":current_asset})



    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
        context = {"user":request.user}
        return HttpResponseRedirect(reverse('IndexView'))

def add_asset(request):
    if request.method == "GET":
        # Show a forum where they can add an asset_value
        form = AssetForm()
        form.fields["owner_portfolio"].queryset = Portfolio.objects.filter(owner=request.user.id)
        context = {"asset_form":form}
        return render(request, 'CMApp/new_asset.html', context)

    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()

        context = {"user":request.user}
        return HttpResponseRedirect(reverse('IndexView'))


def delete_asset(request, asset):
    if request.method == "GET":
        user_portfolio_qs = Portfolio.objects.filter(owner=request.user.id)
        portfolio = user_portfolio_qs[0]
        assets = Asset.objects.filter(owner_portfolio=portfolio)
        current_asset_qs = assets.filter(ticker=asset)
        current_asset = current_asset_qs[0]
        current_asset.delete_asset()
        user_assets = Asset.objects.filter(owner_portfolio = request.user.id)
        return HttpResponseRedirect(reverse('IndexView'))






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
