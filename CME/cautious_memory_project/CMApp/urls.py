from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
path('', views.index, name="IndexView"),
path('register', views.register, name='register'),
path('add_asset', views.add_asset, name='NewAsset'),
path('new_asset/<str:asset>', views.new_entry, name="NewEntry"),
path('delete_asset/<str:asset>', views.delete_asset, name="DeleteAsset"),
path('edit_entry/<str:entry>', views.edit_entry, name="EditEntry"),


]
