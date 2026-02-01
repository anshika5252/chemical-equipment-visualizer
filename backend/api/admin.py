from django.contrib import admin
from .models import Dataset, EquipmentData

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'upload_date', 'row_count']
    list_filter = ['upload_date']
    search_fields = ['filename']

@admin.register(EquipmentData)
class EquipmentDataAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']
    list_filter = ['equipment_type']
    search_fields = ['equipment_name']