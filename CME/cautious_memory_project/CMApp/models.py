from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, post_delete
from django.core.exceptions import ValidationError
from PIL import Image
from django.core.files.images import get_image_dimensions

# Register your models here.

class Portfolio(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name="user_portfolio")


    def __str__(self):
        return "%s's portfolio"  % (self.owner.username)
class Asset(models.Model):
    owner_portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="assets")
    ticker = models.CharField(null=False, max_length=100)
    photo = models.ImageField(default='small.png')
    AHAT = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00')) #Asset Held All Time
    ASAT = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00')) # Asset sold all Time
    FATT = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Fiat Total All Time
    FG = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Fiat gained through Sales
    FCI = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Fiat Current Invested
    CAH = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00')) # Current Asset Held
    CAP = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Current Average price
    APL = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Asset Profit/Loss

    def create_tx(self, type, fiat_arg, asset_arg):
        if type == "Buy":
            self.FATT += fiat_arg
            self.FCI += fiat_arg
            self.AHAT += asset_arg
            self.CAH += asset_arg
            self.save()
            return Transaction(type, fiat_arg, asset_arg)

        if type == "Sell":
            profit_loss = fiat_arg - (asset_arg * self.CAP)
            self.FCI -= (asset_arg * asset.CAP)
            self.CAH -= asset_arg
            self.FG += fiat_arg
            self.ASAT += asset_arg
            self.APL += profit_loss
            self.save()
            return Transaction(type, fiat_arg, asset_arg)

        if type == "Spend":
            self.CAH -= asset_arg
            self.save()
            return Transaction(type, fiat_arg, asset_arg)

        if type == "Acquire":
            self.CAH += asset_arg
            self.save()
            return Transaction(type, fiat_arg, asset_arg)






class Transaction(models.Model):
    tx_asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="transactions")
    fiat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    asset_amount = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00'))
    date_created = models.DateTimeField(auto_now_add=True)
    TX_TYPE_CHOICES = (
    ("Buy", "Buy"),
    ("Sell", "Sell"),
    ("Spend", "Spend"),
    ("Acquire", "Acquire")
    )
    type = models.CharField(null=False, choices=TX_TYPE_CHOICES, max_length=7, default='Buy')





###USER MODEL SIGNALS###

#Create portfolio upon new user creation
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(owner=instance)
    return
post_save.connect(create_user_portfolio, sender=User)

###Asset Model Signals###
def adjust_CAP(sender, instance, **kwargs):
    try:
        instance.CAP = instance.CAH / instance.FCI
    except ZeroDivisionError:
        instance.CAP = 0
        return
    finally:
        return

post_save.connect(adjust_CAP, sender=Asset)
