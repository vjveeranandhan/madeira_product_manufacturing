from rest_framework import serializers
from .models import Order, OrderImage

class OrderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderImage
        fields = ['id', 'image']

class OrderSerializer(serializers.ModelSerializer):
    images = OrderImageSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    # material_ids = serializers.ListField(child=serializers.IntegerField())
    class Meta:
        model = Order
        fields = '__all__'