from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('vendors/', VendorView.as_view(), name='vendor'),
    path('vendors/<int:vendor_id>/', VendorProfileDetailView.as_view(), name='vendor-detail'),
    
]