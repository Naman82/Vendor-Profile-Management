from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
]