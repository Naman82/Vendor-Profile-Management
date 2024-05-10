from django.shortcuts import render
from rest_framework.views import APIView
from users.models import User,Vendor
from .serializers import PurchaseOrderSerializer
from orders.models import PurchaseOrder
from vendorManagementBackend.utils import send_response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone

class PurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'po_number': openapi.Schema(type=openapi.TYPE_STRING, description='po_number'),
                'vendor_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='vendor'),
                'order_date': openapi.Schema(type=openapi.TYPE_STRING, description='order_date'),
                'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, description='delivery_date'),
                'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT), description='items'),
                'quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description='quantity'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='status'),
                'quality_rating': openapi.Schema(type=openapi.TYPE_NUMBER, description='quality_rating'),
                'issue_date': openapi.Schema(type=openapi.TYPE_STRING, description='issue_date'),
                'acknowledgment_date': openapi.Schema(type=openapi.TYPE_STRING, description='acknowledgment_date'),
            },
        ),
        responses={
            200: "Purchase Order Created",
            400: "not valid",
        }
    )
    def post(self, request):
        try:
            data = request.data
            po_number = data.get('po_number')
            vendor_id = data.get('vendor_id')
            order_date = data.get('order_date')
            delivery_date = data.get('delivery_date')
            items = data.get('items')
            quantity = data.get('quantity')
            status = data.get('status')
            quality_rating = data.get('quality_rating')
            issue_date = data.get('issue_date')
            acknowledgment_date = data.get('acknowledgment_date')

            print(data)
            if not po_number or not vendor_id or not order_date or not delivery_date or not items or not quantity or not status or not issue_date:
                return send_response(result=False,message='All fields are required')
            
            if not Vendor.objects.filter(id=vendor_id).exists():
                return send_response(result=False,message='Vendor does not exist')
            
            vendor = Vendor.objects.get(id=vendor_id)
            purchase_order = PurchaseOrder.objects.create(po_number=po_number,vendor=vendor,order_date=order_date,delivery_date=delivery_date,items=items,quantity=quantity,status=status,quality_rating=quality_rating,issue_date=issue_date,acknowledgment_date=acknowledgment_date)
            return send_response(result=True,message='Purchase Order Created')
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    @swagger_auto_schema(
        responses={
            200: "Purchase Order List",
            400: "not valid",
        }
    )
    def get(self, request, format=None):
        try:
            vendor_id = request.query_params.get('vendor_id')
            if vendor_id:
                if not Vendor.objects.filter(id=vendor_id).exists():
                    return send_response(result=False,message='Vendor does not exist')
                vendor = Vendor.objects.get(id=vendor_id)
                purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            else:
                purchase_orders = PurchaseOrder.objects.all()

            serializer = PurchaseOrderSerializer(purchase_orders, many=True)
            data = serializer.data
            return send_response(result=True,message='Purchase Order List',data=data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    
    

class PurchaseOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={
            200: "Purchase Order Details",
            400: "not valid",
        }
    )   
    def get(self, request, po_id):
        try:
            if not PurchaseOrder.objects.filter(id=po_id).exists():
                return send_response(result=False,message='Purchase Order does not exist')
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            serializer = PurchaseOrderSerializer(purchase_order)
            data = serializer.data
            return send_response(result=True,message='Purchase Order Details',data=data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'po_number': openapi.Schema(type=openapi.TYPE_STRING, description='po_number'),
                'vendor_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='vendor'),
                'order_date': openapi.Schema(type=openapi.TYPE_STRING, description='order_date'),
                'delivery_date': openapi.Schema(type=openapi.TYPE_STRING, description='delivery_date'),
                'items': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT), description='items'),
                'quantity': openapi.Schema(type=openapi.TYPE_NUMBER, description='quantity'),
                'status': openapi.Schema(type=openapi.TYPE_STRING, description='status'),
                'quality_rating': openapi.Schema(type=openapi.TYPE_NUMBER, description='quality_rating'),
                'issue_date': openapi.Schema(type=openapi.TYPE_STRING, description='issue_date'),
                'acknowledgment_date': openapi.Schema(type=openapi.TYPE_STRING, description='acknowledgment_date'),
            },
            required=['po_number', 'vendor', 'order_date', 'delivery_date', 'items', 'quantity', 'status', 'issue_date']
        ),
        responses={
            200: "Purchase Order Updated",
            400: "not valid",
        }
    )
    def put(self, request, po_id):
        try:
            data = request.data
            if not PurchaseOrder.objects.filter(id=po_id).exists():
                return send_response(result=False,message='Purchase Order does not exist')
            if not Vendor.objects.filter(id=data.get('vendor_id')).exists():
                return send_response(result=False,message='Vendor does not exist')
            vendor = Vendor.objects.get(id=data.get('vendor_id'))
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.po_number = data.get('po_number')
            purchase_order.vendor = vendor
            purchase_order.order_date = data.get('order_date')
            purchase_order.delivery_date = data.get('delivery_date')
            purchase_order.items = data.get('items')
            purchase_order.quantity = data.get('quantity')
            purchase_order.status = data.get('status')
            purchase_order.quality_rating = data.get('quality_rating')
            purchase_order.issue_date = data.get('issue_date')
            purchase_order.acknowledgment_date = data.get('acknowledgment_date')
            purchase_order.save()
            return send_response(result=True,message='Purchase Order Updated')
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    @swagger_auto_schema(
        responses={
            200: "Purchase Order Deleted",
            400: "not valid",
        }
    )
    def delete(self, request, po_id):
        try:
            if not PurchaseOrder.objects.filter(id=po_id).exists():
                return send_response(result=False,message='Purchase Order does not exist')
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.delete()
            return send_response(result=True,message='Purchase Order Deleted')
        except Exception as e:
            return send_response(result=False, message=str(e))
    
class AcknowledgePurchaseOrderView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        responses={
            200: "Purchase Order Acknowledged",
            400: "not valid",
        }
    )
    def post(self, request, po_id):
        try:
            if not PurchaseOrder.objects.filter(id=po_id).exists():
                return send_response(result=False,message='Purchase Order does not exist')
            purchase_order = PurchaseOrder.objects.get(id=po_id)
            purchase_order.acknowledgment_date = timezone.now()
            purchase_order.save()
            return send_response(result=True,message='Purchase Order Acknowledged')
        except Exception as e:
            return send_response(result=False, message=str(e))