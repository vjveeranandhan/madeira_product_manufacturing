from rest_framework import serializers
from .models import Material

class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'name', 'description', 'colour', 'quality', 'durability', 'stock_availability', 'category', 'price', 'quantity']
