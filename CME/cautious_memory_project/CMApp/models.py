from django.db import models
from django.contrib.auth.models import User

# Register your models here.

class Portfolio(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Asset(models.Model):
    owner_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="assets")
    ticker = models.CharField(null=False, max_length=100)
    fiat = models.DecimalField(max_digits=12, decimal_places=2) ##nine hundred ninety nine billion
    asset = models.DecimalField(max_digits=12, decimal_places=8) # A decimal places to represent a sat
    price_avg = models.DecimalField(max_digits=12, decimal_places=2)
    
class Entry(models.Model):
    pass
    # Tx Type, Asset, Date, Fiat Value, Amount Asset
