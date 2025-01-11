from rest_framework import serializers
from .models import Process

class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ['id', 'name', 'name_mal', 'description', 'description_mal']
