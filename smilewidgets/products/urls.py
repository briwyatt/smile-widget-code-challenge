from django.urls import path
from . import views


urlpatterns = [
    path('get-price', views.get_price, name='get_price')
]
