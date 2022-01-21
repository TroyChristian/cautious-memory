from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
path('', views.index, name="IndexView"),
path('register', views.register, name='register'),
path('add_asset', views.add_asset, name='NewAsset'),
path('new_entry/<str:asset>/<int:asset_id>', views.new_tx, name="NewEntry"),
path('delete_asset/<str:asset>/<int:asset_id>', views.delete_asset, name="DeleteAsset"),
# path('edit_entry/<str:entry>', views.edit_entry, name="EditEntry"),
path('delete_entry/<str:asset>/<int:tx_id>', views.delete_entry, name="DeleteEntry"),
path('export/<int:asset_id>', views.export_asset_csv, name="ExportAsset"),


]
