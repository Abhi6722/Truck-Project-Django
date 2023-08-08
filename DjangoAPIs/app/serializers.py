from rest_framework import serializers
from .models import truckmodel, sku_model


class sku_serializers(serializers.ModelSerializer):
    class Meta:
        model=sku_model
        fields = '__all__'# ('truck_id', 'sku', 'quantity')

class truck_serializers(serializers.ModelSerializer):
    truck = sku_serializers(read_only = True, many=True)
    class Meta:
        model=truckmodel
        fields = '__all__'#('truck_id', 'image_url', 'entry_time', 'exit_time', 'status')
        
