from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Register your models here.

class Portfolio(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    owner

    def __str__(self):
        return "%s's portfolio" % (self.owner.username)

class Asset(models.Model):
    owner_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="assets")
    ticker = models.CharField(null=False, max_length=100)
    fiat = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) ##nine hundred ninety nine billion
    asset = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00000000')) # A decimal places to represent a sat
    price_avg = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))


class Journal(models.Model):
    tracked_asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="journal", primary_key=True)


class Entry(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    # Tx Type, Asset, Date, Fiat Value, Amount Asset
