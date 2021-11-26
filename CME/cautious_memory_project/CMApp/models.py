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
    fiat = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00')) ##nine hundred ninety nine billion
    asset = models.DecimalField(max_digits=12, decimal_places=8, default=Decimal('0.00')) # A decimal places to represent a sat
    price_avg = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    photo = models.ImageField(default='small.png')


    def save(self, *args, **kwargs):
        super(Asset, self).save(*args, **kwargs)
        SIZE = 100,100

        if self.photo:
            pic = Image.open(self.photo.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.photo.path, "PNG")





    def snapshot(self):

        snapshot = self.journal.sum_entries()
        if snapshot:
            (self.fiat, self.asset, self.price_avg) = snapshot #unpack tuple values into asset
            self.save()
            return
        return # means there are no entries for this asset to sum, return

    def delete_asset(self):
        asset_qs = Asset.objects.get(id__exact=self.id)
        asset_qs.delete()
        return


    def __str__(self):
        return "Asset: %s \n Belongs To: %s"% (self.ticker, self.owner_portfolio)


class Journal(models.Model):
    tracked_asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="journal", primary_key=True)

    def sum_entries(self):
        fiat = 0
        asset = 0
        avg_price = 0
        entry_qs = Entry.objects.get_queryset().filter(journal=self).order_by('-entry_type')
        if  not entry_qs:
            return (0,0,0)
        for entry in entry_qs:
            fiat += entry.fiat_value
            asset += entry.asset_value

        try:
            avg_price = fiat / asset
            return (fiat, asset, avg_price)
        except ZeroDivisionError:
            return (0,0,0)
        except:
            return (0,0,0)
        finally:
            if fiat < 0:
                return (0,0,0)
            if asset < 0:
                return (0,0,0)





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
    price_of_asset = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    def update_entry(self, fiat=None, asset=None, type=None):
        try:
            if fiat != None:
                self.fiat_value = Decimal(fiat)
            if asset != None:
                self.asset_value = Decimal(asset)
            if type != None and type == 'credit' or type =='debit':
                self.entry_type = type # Switch type

        except Exception as  error:
            print("An error occured:%s" % error)
            return
        try:
            self.save()
        except Exception as error:
            print("An error occured:%s" % error)
        finally:
            journal = self.journal
            asset = journal.tracked_asset
            asset.snapshot() #create the snapshot after the edited entry is saved
            return

    def delete_entry(self):
        entry = Entry.objects.get(id__exact=self.id)
        entry.delete()
        journal = self.journal
        asset = journal.tracked_asset
        asset.snapshot()
        return






    def __str__(self):
        return " Entry in %s" % (self.journal)

    def clean(self):
        journal = self.journal
        asset = journal.tracked_asset
        if self.fiat_value == 0 or self.asset_value == 0:
            raise ValidationError('Fiat and Asset values must be greater than zero')
        
        if self.entry_type == 'debit':
            if self.fiat_value > asset.fiat or self.asset_value > asset.asset:
                raise ValidationError("You cannot debit more than your total fiat or asset values.")
                print("TRIGGERED")
        else:
            print("SKIPPED")
        return


###ENTRY MODEL SIGNALS###
def make_debits_negative(sender, instance, **kwargs):
    if instance.entry_type == "credit":
            signed_fiat_value = abs(instance.fiat_value)
            signed_asset_value = abs(instance.asset_value)
                #assign positive values
            instance.fiat_value = signed_fiat_value
            instance.asset_value = signed_asset_value
    else:
        signed_fiat_value = -instance.fiat_value
        signed_asset_value = -instance.asset_value
            #assign signed values
        instance.fiat_value = signed_fiat_value
        instance.asset_value = signed_asset_value

    return
pre_save.connect(make_debits_negative, sender=Entry)




def calculate_price_of_asset(sender, instance, **kwargs):
    price_of_asset = instance.fiat_value / instance.asset_value
    instance.price_of_asset = Decimal(price_of_asset)
    return
pre_save.connect(calculate_price_of_asset, sender=Entry)

def calculate_snapshot_upon_new_entry(sender, instance, created, **kwargs):
    instance_journal = instance.journal
    instance_tracked_asset = instance_journal.tracked_asset
    instance_tracked_asset.snapshot()
    return
post_save.connect(calculate_snapshot_upon_new_entry, sender=Entry)

# def calculate_snapshot_upon_entry_deletion(sender, instance, **kwargs):
#     instance_journal = instance.journal
#     instance_tracked_asset = instance_journal.tracked_asset
#     instance_tracked_asset.snapshot()
#     return
# post_delete.connect(calculate_snapshot_upon_entry_deletion, sender=Entry)






###USER MODEL SIGNALS###

#Create portfolio upon new user creation
def create_user_portfolio(sender, instance, created, **kwargs):
    if created:
        Portfolio.objects.create(owner=instance)
    return
post_save.connect(create_user_portfolio, sender=User)


###ASSET MODEL SIGNALS###
def create_asset_journal(sender, instance, created, **kwargs):
    if created:
        Journal.objects.create(tracked_asset=instance)
    return
post_save.connect(create_asset_journal, sender=Asset)
