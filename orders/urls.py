from django.urls import path
from .views import *

urlpatterns = [
    path('purchase_orders/', PurchaseOrderView.as_view(), name='purchase_orders'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderDetailView.as_view(), name='purchase_order-detail'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge_purchase_order'),
]