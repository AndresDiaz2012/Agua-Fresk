from django.db import models


class MessageLog(models.Model):
    STATUS_SENT = 'sent'
    STATUS_DELIVERED = 'delivered'
    STATUS_READ = 'read'
    STATUS_FAILED = 'failed'

    STATUS_CHOICES = (
        (STATUS_SENT, 'Enviado'),
        (STATUS_DELIVERED, 'Entregado'),
        (STATUS_READ, 'Leído'),
        (STATUS_FAILED, 'Fallido'),
    )

    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, related_name='messages')
    provider_message_id = models.CharField(max_length=255, blank=True)
    template_name = models.CharField(max_length=120)
    payload = models.JSONField(default=dict)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_SENT)
    error_detail = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self) -> str:
        return f"Message to {self.customer.full_name} - {self.template_name} - {self.status}"


# Create your models here.
