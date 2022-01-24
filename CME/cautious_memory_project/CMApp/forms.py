from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from . models import  Asset, Portfolio, Transaction
from decimal import Decimal

class LoginForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput)






class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1']
        )
        return user




class TxForm(ModelForm):

    class Meta:
        model = Transaction
        fields = ['type','asset_amount', 'fiat_amount', 'tx_asset']
        fiat_amount = forms.DecimalField(max_digits=12, decimal_places=2)
        asset_amount = forms.DecimalField(max_digits=12, decimal_places=8)
        widgets = {'tx_asset': forms.HiddenInput()}







class AssetForm(ModelForm):

    class Meta:
        model = Asset
        fields = ['ticker', 'owner_portfolio', 'photo']
        widgets = {'owner_portfolio': forms.HiddenInput()}
