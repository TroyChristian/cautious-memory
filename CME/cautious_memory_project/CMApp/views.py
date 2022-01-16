from django.shortcuts import render, HttpResponse, redirect
from . forms import  CustomUserCreationForm, AssetForm, TxForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import Asset, Portfolio, Transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from PIL import Image



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

def add_asset(request):
    if request.method == "GET":
        # Show a forum where they can add an asset_value
        owner_portfolio = Portfolio.objects.filter(owner=request.user.id).get()
        #owner_portfolio = owner_portfolio_qs[0]
        form = AssetForm(initial={'owner_portfolio':owner_portfolio})


        context = {"asset_form":form}
        return render(request, 'CMApp/new_asset.html', context)

    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        else:
            print("Form is not validating")



        context = {"user":request.user}
        return HttpResponseRedirect(reverse('IndexView'))


def new_tx(request, asset, asset_id):
    if request.method == "GET":
        portfolio = Portfolio.objects.filter(owner=request.user.id).get()
        assets = Asset.objects.filter(owner_portfolio=portfolio)
        current_asset = assets.filter(pk=asset_id).get()
        form = TxForm(initial = {'tx_asset':asset_id})
        entry_qs = Transaction.objects.filter(tx_asset=asset_id)
        tx_entries = list(entry_qs)

        return render(request, 'CMApp/new_entry.html', {"entry_form":form, "asset":current_asset, "entries":tx_entries})

    if request.method == "POST":
        form = TxForm(request.POST)


        if form.is_valid():
            form.save()
            context = {"user":request.user}

            return HttpResponseRedirect(reverse('NewEntry', kwargs={'asset':asset, 'asset_id':asset_id}))

        return HttpResponseRedirect(reverse('NewEntry', kwargs={'asset':asset, 'asset_id':asset_id}))





        return render(request, 'CMApp/new_entry.html', {"entry_form":form, "asset":current_asset,})
def delete_entry(request, asset, tx_id):
    current_entry = Transaction.objects.filter(id=tx_id).get()
    asset = current_entry.tx_asset.ticker
    asset_id = current_entry.tx_asset.id
    current_entry.delete()
    return HttpResponseRedirect(reverse('NewEntry', kwargs={'asset':asset, "asset_id":asset_id}))

def delete_asset(request, asset, asset_id):
    if request.method == "GET":
        user_portfolio_qs = Portfolio.objects.filter(owner=request.user.id)
        portfolio = user_portfolio_qs[0]
        assets = Asset.objects.filter(owner_portfolio=portfolio)
        current_asset_qs = assets.filter(pk=asset_id)
        current_asset = current_asset_qs[0]
        current_asset.delete_asset()
        #user_assets = Asset.objects.filter(owner_portfolio = request.user.id)
        return HttpResponseRedirect(reverse('IndexView'))
