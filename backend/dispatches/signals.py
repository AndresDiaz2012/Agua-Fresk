from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Dispatch


@receiver(post_save, sender=Dispatch)
def update_customer_last_dispatch(sender, instance: Dispatch, created: bool, **kwargs):
    customer = instance.customer
    if instance.delivered_at:
        date_to_set = instance.delivered_at.date()
    else:
        date_to_set = instance.scheduled_at.date()

    if customer.last_dispatch_date is None or date_to_set > customer.last_dispatch_date:
        customer.last_dispatch_date = date_to_set
        customer.save(update_fields=['last_dispatch_date'])
