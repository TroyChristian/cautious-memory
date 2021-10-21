from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime

# Register your models here.

class Portfolio(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)


    def __str__(self):
        return "%s's portfolio" % (self.owner.username)

class Asset(models.Model):
    owner_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="assets")
    ticker = models.CharField(null=False, max_length=100)
    fiat = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) ##nine hundred ninety nine billion
    asset = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00000000')) # A decimal places to represent a sat
    price_avg = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return "Asset: %s \n Belongs To: %s"% (self.ticker, self.owner_portfolio)


class Journal(models.Model):
    tracked_asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="journal", primary_key=True)

    def __str__(self):
        return "%s journal in %s" % (self.tracked_asset.ticker, self.tracked_asset.owner_portfolio)

class Entry(models.Model):
    ENTRY_CHOICES = (
    ("credit", "credit"),
    ("debit", "debit"),
    )
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    entry_type = ENTRY_CHOICES
    date = models.DateField(default=datetime.date.today) #allows user to overide
    fiat_value =  models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    asset_value = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00000000'))




    def __str__(self):
        return " Entry in %s" (self.journal)
