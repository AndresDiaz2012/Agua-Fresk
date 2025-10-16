from rest_framework import viewsets, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import Customer
from .serializers import CustomerSerializer
from accounts.permissions import IsAdminOrReadOnlyRole
from rest_framework.decorators import action
from rest_framework.response import Response
from messaging.whatsapp import WhatsAppClient
from messaging.models import MessageLog


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'is_admin', lambda: False)())


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrReadOnlyRole]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active']
    search_fields = ['full_name', 'phone_e164', 'address']
    ordering_fields = ['full_name', 'last_dispatch_date', 'created_at']

    def get_queryset(self):
        qs = super().get_queryset()
        overdue_only = self.request.query_params.get('overdue_only')
        if overdue_only in ('1', 'true', 'True'):
            from django.utils import timezone
            from datetime import timedelta
            from django.conf import settings
            now = timezone.now()
            cutoff_date = (now - timedelta(days=settings.OVERDUE_DAYS)).date()
            qs = qs.filter(is_active=True).filter(last_dispatch_date__isnull=True) | qs.filter(is_active=True, last_dispatch_date__lt=cutoff_date)
        return qs.distinct()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def send_reminder(self, request, pk=None):
        customer = self.get_object()
        client = WhatsAppClient()
        template = 'overdue_reminder'
        payload = {'name': customer.full_name, 'address': customer.address}
        try:
            resp = client.send_template(customer.phone_e164, template, payload)
            log = MessageLog.objects.create(
                customer=customer,
                template_name=template,
                payload=payload,
                provider_message_id=resp.get('messages', [{}])[0].get('id', ''),
                status=MessageLog.STATUS_SENT,
            )
            return Response({'ok': True, 'log_id': log.id})
        except Exception as exc:
            return Response({'ok': False, 'error': str(exc)}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
