from django.contrib import admin
from django.db import models
from . import models as myModels
# Register your models here.

#class AuthorAdmin(admin.ModelAdmin):
    #pass
#admin.site.register(Author, AuthorAdmin)

@admin.register(myModels.Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    fields = ('owner',)

@admin.register(myModels.Asset)
class AssetAdmin(admin.ModelAdmin):
    fields = ("owner_portfolio", "ticker")

@admin.register(myModels.Journal)
class JournalAdmin(admin.ModelAdmin):
    fields = ("tracked_asset",)

@admin.register(myModels.Entry)
class EntryAdmin(admin.ModelAdmin):
    fields = ("journal", "entry_type", "fiat_value", "asset_value", "date" )
