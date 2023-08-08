from django.db import models

class truckmodel(models.Model):
    # truck_id = models.TextField(primary_key=True)
    # image_url = models.TextField(default=None)
    # entry_time = models.DateTimeField()
    # exit_time = models.DateTimeField(default=None)
    # status = models.CharField(default=None)
    truck_id = models.TextField(primary_key=True)
    image_url = models.TextField(blank=True, null=True, default=None)
    entry_time = models.DateTimeField()
    exit_time = models.DateTimeField(blank=True, null=True, default=None)
    status = models.CharField(max_length=9, blank=True, null=True, default=None)   
    
    class Meta:
        ordering = ['-entry_time']
        db_table = 'trucks_details'

        
class sku_model(models.Model):
    sku = models.TextField(primary_key=True)
    truck = models.ForeignKey(truckmodel, on_delete=models.CASCADE, related_name='truck')
    quantity = models.SmallIntegerField()
    
    class Meta:
        # ordering = ['-id']
        db_table = 'sku_details'