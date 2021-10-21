from django.contrib import admin
from django.db import models
from . import models as myModels
# Register your models here.

#class AuthorAdmin(admin.ModelAdmin):
    #pass
#admin.site.register(Author, AuthorAdmin)

@admin.register(myModels.Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    pass

@admin.register(myModels.Asset)
class AssetAdmin(admin.ModelAdmin):
    pass

@admin.register(myModels.Journal)
class JournalAdmin(admin.ModelAdmin):
    pass

@admin.register(myModels.Entry)
class EntryAdmin(admin.ModelAdmin):
    pass
