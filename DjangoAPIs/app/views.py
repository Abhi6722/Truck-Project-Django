from .models import truckmodel, sku_model
from .serializers import truck_serializers, sku_serializers
from DjangoAPIs.model.sample import execute
from django.http.response import JsonResponse
from django.http import HttpResponseNotFound
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
import os
import asyncio

# @api_view(['GET'])
# def showtruck(request):
#     if request.method == 'GET':
#         results = truckmodel.objects.all()
#         serialize = truck_serializers(results, many=True)
#         return JsonResponse(serialize.data, safe = False)

class TruckList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        results = truckmodel.objects.all()
        serialize = truck_serializers(results, many=True)
        return JsonResponse(serialize.data, safe = False)        


# @api_view(['GET'])
# def showsku(request):
#     if request.method == 'GET':
#         results = sku_model.objects.all()
#         serialize = sku_serializers(results, many=True)
#         return JsonResponse(serialize.data, safe = False)

class SKU_List(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        results = sku_model.objects.all()
        serialize = sku_serializers(results, many=True)
        return JsonResponse(serialize.data, safe = False)       
    
     
# @api_view(['GET'])
# def entry_datetime(request, tid):
#     if request.method == 'GET':
#         results = truckmodel.objects.filter(truck_id = tid)
#         serialize = truck_serializers(results, many=True)
#         object = serialize.data[0]['entry_time']
#         object = object.replace('T', ' ').replace('Z','')
#         object = datetime.strptime(object, "%Y-%m-%d %H:%M:%S")
#         entry_date = object.strftime("%d-%m-%Y")
#         entry_time = object.strftime("%I:%M:%S %p")
#         response = {"entry_date": entry_date,
#                     "entry_time": entry_time}
#         return JsonResponse(response, safe = False)

class Entry_Datetime(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, tid):
        try:
            results = truckmodel.objects.get(truck_id = tid)
            # print(results)
            # serialize = truck_serializers(results, many=True)
            # print(serialize.data)
            object = results.entry_time
            # object = serialize.data[0]['entry_time']
            # object = object.replace('T', ' ').replace('Z','')
            # object = datetime.strptime(object, "%Y-%m-%d %H:%M:%S")
            entry_date = object.strftime("%d-%m-%Y")
            entry_time = object.strftime("%I:%M:%S %p")
            response = {"entry_date": entry_date,
                        "entry_time": entry_time}
            return JsonResponse(response, safe = False)
        except truckmodel.DoesNotExist as e:
            return HttpResponseNotFound("truck_id doesn't exist")       


# @api_view(['GET'])
# def latest_truck_entered(request):
#     if request.method == 'GET':
#         object = truckmodel.objects.first()
#         result = getattr(object, 'truck_id')
#         return JsonResponse({"truck_id":result}, safe = False)

class Latest_Truck_Entered(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        object = truckmodel.objects.first()
        result = getattr(object, 'truck_id')
        return JsonResponse({"truck_id":result}, safe = False)       


# @api_view(['GET'])
# def exit_time(request, tid):
#     if request.method == 'GET':
#         results = truckmodel.objects.filter(truck_id = tid)
#         serialize = truck_serializers(results, many=True)
#         object = serialize.data[0]['exit_time']
#         object = object.replace('T', ' ').replace('Z','')
#         object = datetime.strptime(object, "%Y-%m-%d %H:%M:%S")
#         exit_time = object.strftime("%I:%M:%S %p")
#         response = {"exit_time": exit_time}
#         return JsonResponse(response, safe = False)
 
class Exit_Time(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, tid):
        try:
            results = truckmodel.objects.get(truck_id = tid)
            object = results.exit_time
            # serialize = truck_serializers(results, many=True)
            # object = serialize.data[0]['exit_time']
            # object = object.replace('T', ' ').replace('Z','')
            # object = datetime.strptime(object, "%Y-%m-%d %H:%M:%S")
            exit_time = object.strftime("%I:%M:%S %p")
            response = {"exit_time": exit_time}
            return JsonResponse(response, safe = False)
        except truckmodel.DoesNotExist as e:
            return HttpResponseNotFound("truck_id doesn't exist")       
 
    
# @api_view(['GET'])
# def trucks_inside(request):
#     if request.method == 'GET':
#         results = truckmodel.objects.filter(exit_time = None)
#         serialize = truck_serializers(results, many=True)
#         response = {"trucks_inside":serialize.data,
#                     "number of trucks": len(serialize.data)}
#         return JsonResponse(response, safe = False)
 
class Trucks_Inside(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        results = truckmodel.objects.filter(exit_time = None)
        serialize = truck_serializers(results, many=True)
        for dct in serialize.data:
            object = dct['entry_time']
            object = object.replace('T', ' ').replace('Z','')
            object = datetime.strptime(object, "%Y-%m-%d %H:%M:%S")
            dct['entry_date'] = object.strftime("%d-%m-%Y")
            dct['entry_time'] = object.strftime("%I:%M:%S %p")
        response = {"trucks_inside":serialize.data,
                    "number of trucks": len(serialize.data)}
        return JsonResponse(response, safe = False)       
 
    
# @api_view(['GET'])
# def sku_details(request, tid):
#     if request.method == 'GET':
#         results = sku_model.objects.filter(truck_id = tid)
#         serialize = sku_serializers(results, many=True)
#         object = serialize.data
#         return JsonResponse(object, safe = False)

class SKU_Details(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, tid):
        results = sku_model.objects.filter(truck_id = tid)
        serialize = sku_serializers(results, many=True)
        object = serialize.data
        return JsonResponse(object, safe = False)        

   
# @api_view(['POST'])
# def insert_truck_details(request):
#     if request.method == 'POST':
#         saveserialize = truck_serializers(data = request.data)
#         if not saveserialize.is_valid():
#             print(saveserialize.errors)
#             return Response({'status':403, 'errors': saveserialize.errors, 'message':'Something Went Wrong !!'})
        
#         saveserialize.save()
#         return Response({'status':200, 'data': saveserialize.data, 'message':'Data inserted successfully'})

class Insert_Truck_Details(APIView):
    def post(self, request):
        saveserialize = truck_serializers(data = request.data)
        if not saveserialize.is_valid():
            print(saveserialize.errors)
            return Response({'status':403, 'errors': saveserialize.errors, 'message':'Something Went Wrong !!'})
        
        saveserialize.save()
        return Response({'status':200, 'data': saveserialize.data, 'message':'Data inserted successfully'})        

# @api_view(['POST'])
# def insert_sku_details(request):
#     saveserialize = sku_serializers(data = request.data)
#     if not saveserialize.is_valid():
#         print(saveserialize.errors)
#         return Response({'status':403, 'errors': saveserialize.errors, 'message':'Something Went Wrong !!'})
#     saveserialize.save()
#     return Response({'status':200, 'data': saveserialize.data, 'message':'Data inserted successfully'})

class Insert_SKU_Details(APIView):
    def post(self, request):
        saveserialize = sku_serializers(data = request.data)
        if not saveserialize.is_valid():
            print(saveserialize.errors)
            return Response({'status':403, 'errors': saveserialize.errors, 'message':'Something Went Wrong !!'})
        saveserialize.save()
        return Response({'status':200, 'data': saveserialize.data, 'message':'Data inserted successfully'})       

class RecordUpdateView(RetrieveUpdateAPIView):
    serializer_class = truck_serializers
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request, tid):
        try:
            record = truckmodel.objects.get(truck_id=tid)
            # Update loading_status if present in the request
            if 'status' in request.data:
                record.status = request.data['status']

            # Save the updated record
            record.save()

            # Serialize the updated record and return the response
            serializer = self.get_serializer(record, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        except truckmodel.DoesNotExist as e:
            return HttpResponseNotFound("truck_id doesn't exist")
            
class text_rekognition(APIView):
    def post(self, request):
        picture = request.data['picture']
        truckId, entry_datetime, filename  = asyncio.run(execute(picture))
        # Updating S3 link to database
        AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN')
        if truckmodel.objects.filter(truck_id = truckId).exists():
            truck = get_object_or_404(truckmodel, pk=truckId)
            truck.entry_time = entry_datetime
        else:
            truck = truckmodel.objects.create(truck_id = truckId,
                                            image_url=f'https://{AWS_S3_CUSTOM_DOMAIN}/{filename}',
                                            entry_time = entry_datetime)
        truck.save()
        if len(truckId):
            return Response({'text': truckId}, status = status.HTTP_201_CREATED)
        else:
            Response({'message':'No text detected, Upload clear image.'}, status = status.HTTP_403_FORBIDDEN)