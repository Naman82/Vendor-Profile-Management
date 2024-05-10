from django.shortcuts import render
from rest_framework.views import APIView
from .models import User, Vendor
from vendorManagementBackend.utils import send_response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser,FormParser
from .serializers import TokenSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Avg,F
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password')
            },
            required=['email', 'password']
        ),
        responses={
            200: "User Created",
            400: "not valid",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if not data['email'] or not data['password']:
                return send_response(result=False,message='email and password are required')
            if User.objects.filter(email=data['email']).exists():     
                return send_response(result=False,message='User already exists')
            user = User.objects.create_user(email=data['email'],password=data['password'])
            return send_response(result=True,message='User Created')
        except Exception as e:
            return send_response(result=False, message=str(e))

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            },
            required=['email', 'password']
        ),
        responses={
            200: TokenSerializer,
            400: "not valid",
        }
    )
    def post(self, request):
        try:
            data = request.data
            if not data['email'] or not data['password']:
                return send_response(result=False,message='email and password are required')
            if not User.objects.filter(email=data['email']).exists():
                return send_response(result=False,message='User does not exist')
            user = User.objects.get(email=data['email'])
            if not user.check_password(data['password']):
                return send_response(result=False,message='Incorrect Password')
            refresh = RefreshToken.for_user(user)
            return Response(TokenSerializer({
                            'refresh': str(refresh),
                            'access': str(refresh.access_token)
                            } ).data, status=status.HTTP_200_OK)
        except Exception as e:
            return send_response(result=False, message=str(e))

class VendorView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='name'),
                'contact_details': openapi.Schema(type=openapi.TYPE_STRING, description='contact_details'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='address'),
                'vendor_code': openapi.Schema(type=openapi.TYPE_STRING, description='vendor_code'),
                'on_time_delivery_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='on_time_delivery_rate'),
                'quality_rating_avg': openapi.Schema(type=openapi.TYPE_NUMBER, description='quality_rating_avg'),
                'average_response_time': openapi.Schema(type=openapi.TYPE_NUMBER, description='average_response_time'),
                'fulfillment_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='fulfillment_rate'),
            },
        ),
        responses={
            200: "Vendor Created",
            400: "not valid",
        }
    )

    def post(self, request):
        try:
            data = request.data
            name = data.get('name')
            contact_details = data.get('contact_details')
            address = data.get('address')
            vendor_code = data.get('vendor_code')
            on_time_delivery_rate = data.get('on_time_delivery_rate')
            quality_rating_avg = data.get('quality_rating_avg')
            average_response_time = data.get('average_response_time')
            fulfillment_rate = data.get('fulfillment_rate')

            print(type(name), type(contact_details), type(address), type(vendor_code), type(on_time_delivery_rate), type(quality_rating_avg), type(average_response_time), type(fulfillment_rate))
            vendor = Vendor.objects.create(name=name,contact_details=contact_details,address=address,vendor_code=vendor_code,on_time_delivery_rate=on_time_delivery_rate,quality_rating_avg=quality_rating_avg,average_response_time=average_response_time,fulfillment_rate=fulfillment_rate)
            return send_response(result=True,message='Vendor Created')
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    @swagger_auto_schema(
        responses={
            200: "Vendor List",
            400: "not valid",
        }
    )
    def get(self, request):
        try:
            vendors = Vendor.objects.all()
            data = []
            for vendor in vendors:
                data.append({
                    'name': vendor.name,
                    'contact_details': vendor.contact_details,
                    'address': vendor.address,
                    'vendor_code': vendor.vendor_code,
                    'on_time_delivery_rate': vendor.on_time_delivery_rate,
                    'quality_rating_avg': vendor.quality_rating_avg,
                    'average_response_time': vendor.average_response_time,
                    'fulfillment_rate': vendor.fulfillment_rate
                })
            return send_response(result=True,message='Vendor List',data=data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    
        

class VendorProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    
    @swagger_auto_schema(
        responses={
            200: "Vendor Details",
            400: "not valid",
        }
    )
    def get(self, request, vendor_id):
        try:
            if not Vendor.objects.filter(id=vendor_id).exists():
                return send_response(result=False,message='Vendor does not exist')
            vendor = Vendor.objects.get(id=vendor_id)
            data = {
                'name': vendor.name,
                'contact_details': vendor.contact_details,
                'address': vendor.address,
                'vendor_code': vendor.vendor_code,
                'on_time_delivery_rate': vendor.on_time_delivery_rate,
                'quality_rating_avg': vendor.quality_rating_avg,
                'average_response_time': vendor.average_response_time,
                'fulfillment_rate': vendor.fulfillment_rate
            }
            return send_response(result=True,message='Vendor Details',data=data)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='name'),
                'contact_details': openapi.Schema(type=openapi.TYPE_STRING, description='contact_details'),
                'address': openapi.Schema(type=openapi.TYPE_STRING, description='address'),
                'vendor_code': openapi.Schema(type=openapi.TYPE_STRING, description='vendor_code'),
                'on_time_delivery_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='on_time_delivery_rate'),
                'quality_rating_avg': openapi.Schema(type=openapi.TYPE_NUMBER, description='quality_rating_avg'),
                'average_response_time': openapi.Schema(type=openapi.TYPE_NUMBER, description='average_response_time'),
                'fulfillment_rate': openapi.Schema(type=openapi.TYPE_NUMBER, description='fulfillment_rate'),
            },
        ),
        responses={
            200: "Vendor Updated",
            400: "not valid",
        }
    )
    def put(self, request, vendor_id):
        try:
            data = request.data
            if not Vendor.objects.filter(id=vendor_id).exists():
                return send_response(result=False,message='Vendor does not exist')
            vendor = Vendor.objects.get(id=vendor_id)
            vendor.name = data.get('name')
            vendor.contact_details = data.get('contact_details')
            vendor.address = data.get('address')
            vendor.vendor_code = data.get('vendor_code')
            vendor.on_time_delivery_rate = data.get('on_time_delivery_rate')
            vendor.quality_rating_avg = data.get('quality_rating_avg')
            vendor.average_response_time = data.get('average_response_time')
            vendor.fulfillment_rate = data.get('fulfillment_rate')
            # vendor.contact_details = data['contact_details']
            # vendor.address = data['address']
            # vendor.vendor_code = data['vendor_code']
            # vendor.on_time_delivery_rate = data['on_time_delivery_rate']
            # vendor.quality_rating_avg = data['quality_rating_avg']
            # vendor.average_response_time = data['average_response_time']
            # vendor.fulfillment_rate = data['fulfillment_rate']
            vendor.save()
            return send_response(result=True,message='Vendor Updated')
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    @swagger_auto_schema(
        responses={
            200: "Vendor Deleted",
            400: "not valid",
        }
    )
    def delete(self, request, vendor_id):
        try:
            if not Vendor.objects.filter(id=vendor_id).exists():
                return send_response(result=False,message='Vendor does not exist')
            vendor = Vendor.objects.get(id=vendor_id)
            vendor.delete()
            return send_response(result=True,message='Vendor Deleted')
        except Exception as e:
            return send_response(result=False, message=str(e))
