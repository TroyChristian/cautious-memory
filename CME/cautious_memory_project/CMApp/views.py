from django.shortcuts import render, HttpResponse, redirect
from . forms import  CustomUserCreationForm, AssetForm, TxForm, LoginForm
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
from . models import Asset, Portfolio, Transaction
from django.core.exceptions import ValidationError
from django.contrib.auth import login, logout
from PIL import Image
from decimal import Decimal
import csv


# Create your views here.


def index(request):
    if request.user.is_authenticated:
        # Fetch a users asset
        user_assets = Asset.objects.filter(owner_portfolio = request.user.id)
        context = {"user":request.user,
                    "assets":user_assets,

                    }

        return render(request, 'CMApp/dashboard.html', context)

    if request.method=="GET":
        return redirect('login')


# def login(request):
#     if request.method == "GET":
#         context = {'form': LoginForm()}
#         return render(request, 'CMApp/login.html', context)
#
#     if request.method == "POST":
#         form = LoginForm(request.POST)
#         #if form.is_valid():
#
#         username = str(form.fields['username'])
#         password = str(form.fields['password'])
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             return HttpResponseRedirect(reverse('IndexView'))
#
#         else:
#             context = {'form': LoginForm()}
#             return HttpResponseRedirect(reverse('IndexView'))
#     return HttpResponseRedirect(reverse('IndexView'))













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
        entry_qs = Transaction.objects.filter(tx_asset_id=asset_id)
        tx_entries = list(entry_qs)

        return render(request, 'CMApp/new_entry.html', {"entry_form":form, "asset":current_asset, "entries":tx_entries})

    if request.method == "POST":
        types_not_allowed_to_have_greater_asset_value_than_CAH = ['Sell', "Spend"]
        portfolio = Portfolio.objects.filter(owner=request.user.id).get()
        assets = Asset.objects.filter(owner_portfolio=portfolio)
        current_asset = assets.filter(pk=asset_id).get()
        entry_qs = Transaction.objects.filter(tx_asset_id=asset_id)
        tx_entries = list(entry_qs)
        form = TxForm(request.POST)

        if form.is_valid():
            if form.cleaned_data['asset_amount'] > current_asset.CAH and form.cleaned_data['type'] in types_not_allowed_to_have_greater_asset_value_than_CAH :
                return  render(request, 'CMApp/new_entry.html', {"entry_form":form, "asset":current_asset, "entries":tx_entries})
            portfolio = Portfolio.objects.filter(owner=request.user.id).get()
            assets = Asset.objects.filter(owner_portfolio=portfolio)
            current_asset = assets.filter(pk=asset_id).get()
            form.save()
            last_tx_qs = Transaction.objects.all()
            tx_list = list(last_tx_qs)
            last_tx = tx_list[-1]
            current_asset.enter_tx(last_tx)
            current_asset.save()



    return HttpResponseRedirect(reverse('NewEntry', kwargs={'asset':asset, 'asset_id':asset_id}))








def delete_entry(request, asset, tx_id):
    current_entry = Transaction.objects.filter(id=tx_id).get()
    asset_ticker = current_entry.tx_asset.ticker
    asset_id = current_entry.tx_asset.id
    asset = Asset.objects.filter(id=asset_id).get()

    asset.delete_tx(tx_id)
    asset.save()
    current_entry.delete()
    return HttpResponseRedirect(reverse('NewEntry', kwargs={'asset':asset, "asset_id":asset_id}))

def delete_asset(request, asset, asset_id):
    if request.method == "GET":
        user_portfolio_qs = Portfolio.objects.filter(owner=request.user.id)
        portfolio = user_portfolio_qs[0]
        assets = Asset.objects.filter(owner_portfolio=portfolio)
        current_asset = assets.filter(pk=asset_id).get()
        current_asset.delete()
        #user_assets = Asset.objects.filter(owner_portfolio = request.user.id)
        return HttpResponseRedirect(reverse('IndexView'))


def export_asset_csv(request, asset_id):
    asset = Asset.objects.filter(id=asset_id).get() # grab the asset
    ticker = asset.ticker
    transaction_qs = Transaction.objects.filter(tx_asset_id=asset_id).values_list('date_created', 'tx_asset', 'type',  'fiat_amount', 'asset_amount',) # Grab the tx's of the asset
    response = HttpResponse(
    content_type='text/csv',
    headers={'Content-Disposition': 'attachment;filename="asset_history.csv"'},
    )
    writer = csv.writer(response)
    writer.writerow(['date_created', ticker, 'type',  'fiat', 'asset',])
    for tx in transaction_qs:
        writer.writerow(tx)
    return response
