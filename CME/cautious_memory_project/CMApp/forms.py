from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.forms import widgets
from django.forms.widgets import Select
from . models import Entry, Asset, Portfolio
from decimal import Decimal

#class UserRegisterForm(UserCreationForm):


class CustomUserCreationForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-control'}))

    

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


class EntryForm(ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_type', 'date', 'fiat_value', 'asset_value', 'journal']
        fiat_value = forms.DecimalField(max_digits=12, decimal_places=2)
        asset_value = forms.DecimalField(max_digits=12, decimal_places=2)
        widgets = {'journal': forms.HiddenInput(), 
                    'entry_type': forms.Select(attrs={'class': 'select'}),
                    'date': forms.DateInput(attrs={'class': 'select'}),
                    'fiat_value': forms.NumberInput(attrs={'class': 'select'}),
                    'asset_value': forms.NumberInput(attrs={'class': 'select'}),           
         }

    




class AssetForm(ModelForm):

    class Meta:
        model = Asset
        fields = ['ticker', 'owner_portfolio']
        widgets = {'owner_portfolio': forms.HiddenInput()}
