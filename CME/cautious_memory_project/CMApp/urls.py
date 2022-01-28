from django.urls import path
from . import views 


urlpatterns = [
#path('login', views.login, name="LoginView"),
path('', views.index, name="IndexView"),
path('register', views.register, name='register'),
path('add_asset', views.add_asset, name='NewAsset'),
path('new_entry/<str:asset>/<int:asset_id>', views.new_tx, name="NewEntry"),
path('delete_asset/<str:asset>/<int:asset_id>', views.delete_asset, name="DeleteAsset"),
path('delete_entry/<str:asset>/<int:tx_id>', views.delete_entry, name="DeleteEntry"),
path('export/<int:asset_id>', views.export_asset_csv, name="ExportAsset"),
path('my_profile/<int:user_id>', views.my_profile, name="MyProfile"),


]
