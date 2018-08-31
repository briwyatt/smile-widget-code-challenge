from rest_framework import serializers
from .models import Product, GiftCard, ProductPrice

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'code')


class GiftCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiftCard
        fields = ('__all__')

class ProductPriceSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='product')

    class Meta:
        model = ProductPrice
        read_only_fields = ('id', 'name')
        fields = ('id', 'name', 'title', 'price', 'date_start', 'date_end')
