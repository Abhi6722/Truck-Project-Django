from django.contrib import admin
from .models import truckmodel, sku_model

# Register your models here.
admin.site.register(truckmodel)
admin.site.register(sku_model)