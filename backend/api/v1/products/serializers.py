from rest_framework import serializers
from apps.products.models import (
    Product,
    Customer,
    Order
)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    product = ProductSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

