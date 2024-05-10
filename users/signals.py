# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import User, Vendor

# @receiver(post_save, sender=User)
# def create_vendor_profile(sender, instance, created, **kwargs):
#     if created:
#         Vendor.objects.create(user=instance)
