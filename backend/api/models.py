from django.db import models
from django.contrib.auth.models import User

class Dataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    row_count = models.IntegerField()
    summary_stats = models.JSONField()
    file = models.FileField(upload_to='uploads/')
    
    class Meta:
        ordering = ['-upload_date']
        
    def __str__(self):
        return f"{self.filename} - {self.upload_date.strftime('%Y-%m-%d %H:%M')}"

class EquipmentData(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment_records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"