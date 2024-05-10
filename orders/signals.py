from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg, F
from django.utils import timezone
from orders.models import PurchaseOrder
from performance.models import HistoricalVendorPerformance
from users.models import Vendor
from django.db.models import Avg, ExpressionWrapper, F, fields

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if not created:
        try:
            vendor = instance.vendor
            completed_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
            if completed_purchase_orders.exists():
                average_response_time = completed_purchase_orders.aggregate(
                    avg_response_time=Avg(F('acknowledgment_date') - F('issue_date'))
                )['avg_response_time']
                
                # Convert timedelta to seconds and then to float
                average_response_time_seconds = average_response_time.total_seconds()
                
                # Assuming average_response_time is a FloatField in HistoricalVendorPerformance
                vendor.historicalvendorperformance_set.update_or_create(
                    vendor=vendor,
                    date=timezone.now().date(),
                    defaults={
                        'average_response_time': average_response_time_seconds,
                    }
                )
        except Exception as e:
            print(f"Error updating average response time: {str(e)}")



@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender,instance,created, **kwargs):
    if not created and instance.status == 'completed':
        try:
            vendor = instance.vendor
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            completed_purchase_orders = purchase_orders.filter(status='completed')
            #Calculate the counts
            total_purchase_orders_count = purchase_orders.count()
            completed_purchase_orders_count = completed_purchase_orders.count()
            
            # Check if denominator is zero
            if total_purchase_orders_count == 0:
                fulfillment_rate = 0
            else:
                fulfillment_rate = (completed_purchase_orders_count / total_purchase_orders_count) * 100
       
            vendor.historicalvendorperformance_set.update_or_create(
                vendor=vendor,
                date=timezone.now().date(),
                defaults={
                    'fulfillment_rate': fulfillment_rate,
                }
            )
        except Exception as e:
            print(f"Error updating fulfillment rate: {str(e)}")

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if not created and instance.status == 'completed':
        try:
            vendor = instance.vendor
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            completed_purchase_orders = purchase_orders.filter(status='completed')
            
            # Filter completed purchase orders with delivery_date <= instance's delivery_date
            on_time_delivery_orders = completed_purchase_orders.filter(delivery_date__lte=F('delivery_date'))
            
            # Calculate on-time delivery rate
            on_time_delivery_orders_count = on_time_delivery_orders.count()
            completed_purchase_orders_count = completed_purchase_orders.count()
            if completed_purchase_orders_count == 0:
                on_time_delivery_rate = 0
            else:
                on_time_delivery_rate = (on_time_delivery_orders.count() / completed_purchase_orders.count()) * 100.0
            
            vendor.historicalvendorperformance_set.update_or_create(
                vendor=vendor,
                date=timezone.now().date(),
                defaults={
                    'on_time_delivery_rate': on_time_delivery_rate,
                }
            )
        except Exception as e:
            print(f"Error updating on time delivery rate: {str(e)}")


@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender,instance,created, **kwargs):
    if not created and instance.status == 'completed':
        try:
            vendor = instance.vendor
            purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
            completed_purchase_orders = purchase_orders.filter(status='completed')
            quality_rating_avg = completed_purchase_orders.aggregate(Avg('quality_rating'))['quality_rating__avg']
            vendor.historicalvendorperformance_set.update_or_create(
                vendor=vendor,
                date=timezone.now().date(),
                defaults={
                    'quality_rating_avg': quality_rating_avg,
                }
            )
        except Exception as e:
            print(f"Error updating quality rating avg: {str(e)}")