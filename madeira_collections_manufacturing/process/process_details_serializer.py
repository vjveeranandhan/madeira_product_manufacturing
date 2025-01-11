from rest_framework import serializers
from process.models import ProcessDetails
from .models import ProcessMaterials

class ProcessDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessDetails
        fields = '__all__'  # Include all fields

class ProcessMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessMaterials
        fields = '__all__'
