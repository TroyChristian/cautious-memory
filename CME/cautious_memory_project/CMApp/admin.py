from django.contrib import admin
from django.db import models
from . import models as myModels
# Register your models here.

#class AuthorAdmin(admin.ModelAdmin):
    #pass
#admin.site.register(Author, AuthorAdmin)

@admin.register(myModels.Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('owner',)


@admin.register(myModels.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("owner_portfolio", "ticker")


@admin.register(myModels.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("tx_asset", "fiat_amount", "asset_amount", "date_created", "type", "tx_profit_loss", "asset_cap_upon_creation")
