from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name="IndexView"),
path('register', views.register, name='register'),
path('add_asset', views.add_asset, name='NewAsset'),
path('new_asset/<str:asset>', views.new_entry, name="NewEntry")

]
