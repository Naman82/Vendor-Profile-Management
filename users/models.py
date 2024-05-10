from email.policy import default
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator
import os, uuid
from .managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return "{}".format(self.email)
    
    def save(self, *args, **kwargs):
        if self.id:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)
    
class Vendor(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    contact_details = models.TextField(default=None)
    address = models.TextField(default=None)
    vendor_code = models.CharField(max_length=255, unique=True)
    on_time_delivery_rate = models.FloatField(validators=[MaxValueValidator(100)], default=0.0)
    quality_rating_avg = models.FloatField(validators=[MaxValueValidator(5)], default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(validators=[MaxValueValidator(100)], default=0.0)

    def __str__(self):
        return "{}".format(self.name)

