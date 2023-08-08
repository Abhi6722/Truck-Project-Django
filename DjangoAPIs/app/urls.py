from django.urls import path
from .views import *

urlpatterns = [
    path('show_truck/',TruckList.as_view(), name='showtruck'),
    path('show_sku/',SKU_List.as_view(), name='showsku'),
    path('entry_datetime/<tid>/',Entry_Datetime.as_view(), name='entry_datetime'),
    path('latest_truck_entered/',Latest_Truck_Entered.as_view(), name='latest_truck_entered'),
    path('exit_time/<tid>/',Exit_Time.as_view(), name='exit_time'),
    path('trucks_inside/',Trucks_Inside.as_view(), name='trucks_inside'),
    path('sku_details/<tid>/',SKU_Details.as_view(), name='sku_details'),
    path('insert_truck_details/',Insert_Truck_Details.as_view(), name='insert_truck_details'),
    path('insert_sku_details/',Insert_SKU_Details.as_view(), name='insert_sku_details'),
    path('update_status/<tid>/',RecordUpdateView.as_view(), name='update_loading_status'),
    path('text_rekognition/',text_rekognition.as_view(), name='text_rekognition'),
]