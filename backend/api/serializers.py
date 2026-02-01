from rest_framework import serializers
from .models import Dataset, EquipmentData

class EquipmentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']

class DatasetSerializer(serializers.ModelSerializer):
    equipment_records = EquipmentDataSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'row_count', 'summary_stats', 'equipment_records']

class DatasetListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ['id', 'filename', 'upload_date', 'row_count', 'summary_stats']