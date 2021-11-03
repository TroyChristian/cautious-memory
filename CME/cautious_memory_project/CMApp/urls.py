from django.urls import path
from . import views
urlpatterns = [
path('', views.index, name="index_view"),
path('register', views.register, name='register'),
path('add_asset', views.add_asset, name='NewAsset'),

]
