from django.shortcuts import render, HttpResponse, redirect
from . forms import EntryForm, CustomUserCreationForm, AssetForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import Asset, Portfolio, Entry, Journal
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout


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
        return HttpResponseRedirect(reverse('login'))

def new_entry(request, asset):
    if request.method == "GET":
        user_portfolio_qs = Portfolio.objects.filter(owner=request.user.id)
        portfolio = user_portfolio_qs[0]
        assets = Asset.objects.filter(owner_portfolio=portfolio)
        current_asset_qs = assets.filter(ticker=asset)
        current_asset = current_asset_qs[0]
        current_asset.snapshot()
        asset_journal_qs = Journal.objects.filter(tracked_asset = current_asset.id)
        asset_journal = asset_journal_qs[0]

        form = EntryForm(initial = {'journal':asset_journal})
        form.fields["journal"].queryset = Journal.objects.filter(tracked_asset = current_asset.id)

        # make a query for entries using the asset_journal
        entry_qs = Entry.objects.filter(journal=asset_journal)
        entries = list(entry_qs)



        return render(request, 'CMApp/new_entry.html', {"entry_form":form, "asset":current_asset, "entries":entries})



    if request.method == "POST":
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            context = {"user":request.user}
            return HttpResponseRedirect(reverse('IndexView'))
        else:
            messages.error(request, "Fiat and Asset Value must be greater than zero")
            return HttpResponseRedirect(reverse('NewEntry', kwargs={'asset':asset}))


def add_asset(request):
    if request.method == "GET":
        # Show a forum where they can add an asset_value
        owner_portfolio_qs = Portfolio.objects.filter(owner=request.user.id)
        owner_portfolio = owner_portfolio_qs[0]
        form = AssetForm(initial={'owner_portfolio':owner_portfolio})


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
