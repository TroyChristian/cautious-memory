from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal
import datetime
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save 

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

    def snapshot(self):

        snapshot = self.journal.sum_entries()
        (self.fiat, self.asset, self.price_avg) = snapshot #unpack tuple values into asset
        self.save()
        return

    def __str__(self):
        return "Asset: %s \n Belongs To: %s"% (self.ticker, self.owner_portfolio)


class Journal(models.Model):
    tracked_asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="journal", primary_key=True)

    def sum_entries(self):
        fiat = 0
        asset = 0
        avg_price = 0
        entry_qs = Entry.objects.get_queryset().filter(journal=self)
        for entry in entry_qs:
            fiat += entry.fiat_value
            asset += entry.asset_value

        avg_price = fiat / asset
        return (fiat, asset, avg_price)




    def __str__(self):
        return "%s journal in %s" % (self.tracked_asset.ticker, self.tracked_asset.owner_portfolio)

class Entry(models.Model):
    ENTRY_CHOICES = (
    ("credit", "credit"),
    ("debit", "debit"),
    )
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)
    entry_type = models.CharField(null=False, choices=ENTRY_CHOICES, max_length=6, default='credit')
    date = models.DateField(default=datetime.date.today) #allows user to overide
    fiat_value =  models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    asset_value = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00000000'))







    def __str__(self):
        return " Entry in %s" % (self.journal)


def make_debits_negative(sender, instance, **kwargs):
    if instance.entry_type == "credit": #if user is adding funds pass, might put a check here if they use a - sign  or validate in in the form
        pass
    else:
        signed_fiat_value = -instance.fiat_value
        signed_asset_value = -instance.asset_value
            #assign signed values
        instance.fiat_value = signed_fiat_value
        instance.asset_value = signed_asset_value
    return
pre_save.connect(make_debits_negative, sender=Entry)

def calculate_snapshot_upon_new_entry(sender, instance, created, **kwargs):
    instance_journal = instance.journal
    instance_tracked_asset = instance_journal.tracked_asset
    instance_tracked_asset.snapshot()
    return
post_save.connect(calculate_snapshot_upon_new_entry, sender=Entry)
