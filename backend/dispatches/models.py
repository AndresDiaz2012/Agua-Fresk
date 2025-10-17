from django.db import models
from django.conf import settings


class Dispatch(models.Model):
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='dispatches')
    scheduled_at = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)
    address_snapshot = models.CharField(max_length=500)
    quantity_liters = models.PositiveIntegerField(default=20)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-scheduled_at']

    def __str__(self) -> str:
        return f"Dispatch to {self.customer.full_name} at {self.scheduled_at}"


# Create your models here.
