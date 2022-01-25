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
    FATT = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Fiat Total Invested All Time
    FG = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Fiat gained through Sales
    FCI = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Fiat Current Invested
    CAH = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00')) # Current Asset Held
    CAP = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Current Average price
    APL = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) # Asset Profit/Loss

    def save(self, *args, **kwargs):
        super(Asset, self).save(*args, **kwargs)
        SIZE = 100,100

        if self.photo:
            pic = Image.open(self.photo.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.photo.path, "PNG")

    def enter_tx(self, tx):
        cap = self.CAP
        cap = cap if cap > 0 else (tx.fiat_amount / tx.asset_amount)
        if tx.type == "Buy":
            self.FATT += tx.fiat_amount
            self.FCI += tx.fiat_amount
            self.AHAT += tx.asset_amount
            self.CAH += tx.asset_amount
            tx.asset_cap_upon_creation = cap

        if tx.type == "Sell":
            profit_loss = tx.fiat_amount - (tx.asset_amount * cap)
            tx.tx_profit_loss = profit_loss
            tx.asset_cap_upon_creation = cap
            self.FCI -= (tx.asset_amount * cap)
            self.CAH -= tx.asset_amount
            self.FG += tx.fiat_amount
            self.ASAT += tx.asset_amount
            self.APL += profit_loss

        if tx.type == "Spend":
            self.CAH -= tx.asset_amount

        if tx.type == "Acquire":
            self.CAH += tx.asset_amount


        self.update_CPA()
        tx.save()
        return



    def delete_tx(self, tx_id):
        tx = Transaction.objects.filter(id=tx_id).get()

        if tx.type == "Buy":
            self.FATT -= tx.fiat_amount
            self.FCI -= tx.fiat_amount
            self.AHAT -= tx.asset_amount
            self.CAH -= tx.asset_amount

        if tx.type == "Sell":
            #self.FCI += tx.fiat_amount
            self.FCI += (tx.asset_amount * tx.asset_cap_upon_creation)
            self.CAH += tx.asset_amount
            self.FG -= tx.fiat_amount
            self.ASAT -= tx.asset_amount
            self.APL -= tx.tx_profit_loss


        if type == "Spend":
            self.CAH += tx.asset_amount

        if type == "Acquire":
            self.CAH -= tx.asset_amount

        self.update_CPA()


        #update current price average (cost basis)
    def update_CPA(self):
        try:
            self.CAP = self.FCI / self.CAH
        except:
            self.CAP = 0
        return




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
    tx_profit_loss = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2, default=Decimal('0.00'))
    asset_cap_upon_creation = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2, default=Decimal('0.00'))

  # ['date_created', 'tx_asset', 'type',  'fiat_amount', 'asset_amount', 'assset_cap_upon_creation', 'tx_profit_loss']



###USER MODEL SIGNALS###

#Create portfolio upon new user creation
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(owner=instance)
    return
post_save.connect(create_user_portfolio, sender=User)
