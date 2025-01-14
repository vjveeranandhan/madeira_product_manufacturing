from rest_framework import serializers
from .models import Order, OrderImage

class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ['id', 'image']

class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
