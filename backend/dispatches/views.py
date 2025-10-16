from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Dispatch
from .serializers import DispatchSerializer
from accounts.permissions import IsAdminRole


class DispatchViewSet(viewsets.ModelViewSet):
    queryset = Dispatch.objects.select_related('customer').all()
    serializer_class = DispatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['customer']
    search_fields = ['customer__full_name', 'address_snapshot']
    ordering_fields = ['scheduled_at', 'delivered_at', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['destroy']:
            return [IsAdminRole()]
        return super().get_permissions()


# Create your views here.
