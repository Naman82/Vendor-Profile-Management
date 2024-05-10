from django.db import models
from users.models import Vendor
from django.core.validators import MaxValueValidator
    

class HistoricalVendorPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(validators=[MaxValueValidator(100)], null=True, blank=True)
    quality_rating_avg = models.FloatField(validators=[MaxValueValidator(5)],null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(validators=[MaxValueValidator(100)], null=True, blank=True)

    def __str__(self):
        return "{}".format(self.vendor.name)