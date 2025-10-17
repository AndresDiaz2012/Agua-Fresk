from datetime import timedelta
from django.utils import timezone
from celery import shared_task
from django.conf import settings
from customers.models import Customer
from .models import MessageLog
from .whatsapp import WhatsAppClient


@shared_task
def send_overdue_reminders_task() -> int:
    now = timezone.now()
    cutoff_date = (now - timedelta(days=settings.OVERDUE_DAYS)).date()
    cooldown_cutoff = now - timedelta(days=settings.ALERT_COOLDOWN_DAYS)

    customers_qs = Customer.objects.filter(is_active=True).filter(
        last_dispatch_date__isnull=True
    ) | Customer.objects.filter(is_active=True, last_dispatch_date__lt=cutoff_date)

    client = WhatsAppClient()
    sent_count = 0
    for customer in customers_qs.distinct():
        last_msg = customer.messages.order_by('-created_at').first()
        if last_msg and last_msg.created_at > cooldown_cutoff:
            continue

        template = 'overdue_reminder'
        payload = {
            'name': customer.full_name,
            'address': customer.address,
        }
        try:
            resp = client.send_template(customer.phone_e164, template, payload)
            MessageLog.objects.create(
                customer=customer,
                template_name=template,
                payload=payload,
                provider_message_id=resp.get('messages', [{}])[0].get('id', ''),
                status=MessageLog.STATUS_SENT,
            )
            sent_count += 1
        except Exception as exc:
            MessageLog.objects.create(
                customer=customer,
                template_name=template,
                payload=payload,
                status=MessageLog.STATUS_FAILED,
                error_detail=str(exc),
            )

    return sent_count
