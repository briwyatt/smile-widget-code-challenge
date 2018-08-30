from django.conf.urls import url
from . import views

urlpatterns = [
    url('get-price', views.get_price, name="get-price"),
]
