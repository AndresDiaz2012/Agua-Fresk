from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import MessageLog
from .serializers import MessageLogSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from .whatsapp import WhatsAppClient


class MessageLogViewSet(viewsets.ModelViewSet):
    queryset = MessageLog.objects.select_related('customer').all()
    serializer_class = MessageLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'template_name']
    search_fields = ['customer__full_name', 'provider_message_id']
    ordering_fields = ['created_at', 'status']

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def resend(self, request, pk=None):
        log = self.get_object()
        client = WhatsAppClient()
        resp = client.send_template(log.customer.phone_e164, log.template_name, log.payload)
        log.provider_message_id = resp.get('messages', [{}])[0].get('id', '')
        log.status = MessageLog.STATUS_SENT
        log.save(update_fields=['provider_message_id', 'status'])
        return Response(MessageLogSerializer(log).data)


# Create your views here.
