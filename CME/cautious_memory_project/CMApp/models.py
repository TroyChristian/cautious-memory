from django.db import models
from django.contrib.auth.models import User

# Register your models here.

class Portfolio(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Asset(models.Model):
    owner_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="assets")
    ticker = models.CharField(null=False, max_length=100)
    #Journal = List of transactions associated with this Asset, in this portfolio
    # Fiat In, Asset In, Average Price In
class Entry(models.Model):
    pass
    # Tx Type, Asset, Date, Fiat Value, Amount Asset
