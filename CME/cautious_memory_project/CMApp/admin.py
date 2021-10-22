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
    #list_editable = ('owner',)

@admin.register(myModels.Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("owner_portfolio", "ticker")


@admin.register(myModels.Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ("tracked_asset",)
    #list_editable = ("tracked_asset",)

@admin.register(myModels.Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ("journal", "entry_type", "fiat_value", "asset_value", "date" )
    #list_editable = ("journal", "entry_type", "fiat_value", "asset_value", "date" )
