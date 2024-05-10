from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from users.models import User,Vendor
from orders.models import PurchaseOrder
from performance.models import HistoricalVendorPerformance
from django.db.models import Avg, F
from vendorManagementBackend.utils import send_response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class VendorPerformanceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: "Vendor Performance Metrics",
            400: "not valid",
        }
    )
    def get(self, request, vendor_id):
        try:
            if not Vendor.objects.filter(id=vendor_id).exists():
                return send_response(result=False,message='Vendor does not exist')
            vendor = Vendor.objects.get(id=vendor_id)
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            completed_purchase_orders = purchase_orders.filter(status='completed')
            on_time_delivery_rate = 0
            quality_rating_avg = 0
            average_response_time = 0
            fulfillment_rate = 0
            if completed_purchase_orders:
                
                on_time_delivery_orders = completed_purchase_orders.filter(delivery_date__lte=F('delivery_date'))
                completed_purchase_orders_count = completed_purchase_orders.count()
                if completed_purchase_orders_count == 0:
                    on_time_delivery_rate = 0
                else:
                    on_time_delivery_rate = (on_time_delivery_orders.count() / completed_purchase_orders.count()) * 100.0

                
                quality_rating_avg = completed_purchase_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']
                average_response_time = completed_purchase_orders.aggregate(
                    avg_response_time=Avg(F('acknowledgment_date') - F('issue_date'))
                )['avg_response_time']
                
                # Convert timedelta to seconds and then to float
                average_response_time_seconds = average_response_time.total_seconds()

                total_purchase_orders_count = purchase_orders.count()
                completed_purchase_orders_count = completed_purchase_orders.count()
                
                # Check if denominator is zero
                if total_purchase_orders_count == 0:
                    fulfillment_rate = 0
                else:
                    fulfillment_rate = (completed_purchase_orders_count / total_purchase_orders_count) * 100
       
            data = {
                'on_time_delivery_rate': on_time_delivery_rate,
                'quality_rating_avg': quality_rating_avg,
                'average_response_time_seconds': average_response_time_seconds,
                'fulfillment_rate': fulfillment_rate
            }
            return send_response(result=True,message='Vendor Performance Metrics',data=data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    
class HistoricalPerformanceView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'date': openapi.Schema(type=openapi.TYPE_STRING, description='date'),
                'on_time_delivery_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='on_time_delivery_rate'),
                'quality_rating_avg': openapi.Schema(type=openapi.TYPE_NUMBER, description='quality_rating_avg'),
                'average_response_time': openapi.Schema(type=openapi.TYPE_NUMBER, description='average_response_time'),
                'fulfillment_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='fulfillment_rate'),
            },
            required=['date', 'on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
        ),
        responses={
            200: "Historical Performance Record Created",
            400: "not valid",
        }
    )
    def post(self, request, vendor_id):
        try:
            data = request.data
            if not Vendor.objects.filter(id=vendor_id).exists():
                return send_response(result=False,message='Vendor does not exist')
            vendor = Vendor.objects.get(id=vendor_id)
            historical_performance = HistoricalVendorPerformance.objects.create(vendor=vendor,date=data['date'],on_time_delivery_rate=data['on_time_delivery_rate'],quality_rating_avg=data['quality_rating_avg'],average_response_time=data['average_response_time'],fulfillment_rate=data['fulfillment_rate'])
            return send_response(result=True,message='Historical Performance Record Created')
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    @swagger_auto_schema(
        responses={
            200: "Historical Performance Records",
            400: "not valid",
        }
    )
    def get(self, request, vendor_id):
        try:
            if not Vendor.objects.filter(id=vendor_id).exists():
                return send_response(result=False,message='Vendor does not exist')
            vendor = Vendor.objects.get(id=vendor_id)
            historical_performances = HistoricalVendorPerformance.objects.filter(vendor=vendor)
            data = []
            for historical_performance in historical_performances:
                data.append({
                    'date': historical_performance.date,
                    'on_time_delivery_rate': historical_performance.on_time_delivery_rate,
                    'quality_rating_avg': historical_performance.quality_rating_avg,
                    'average_response_time': historical_performance.average_response_time,
                    'fulfillment_rate': historical_performance.fulfillment_rate

                })
            return send_response(result=True,message='Historical Performance Records',data=data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    
