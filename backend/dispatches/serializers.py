from rest_framework import serializers
from .models import Dispatch


class DispatchSerializer(serializers.ModelSerializer):
    customer_full_name = serializers.CharField(source='customer.full_name', read_only=True)

    class Meta:
        model = Dispatch
        fields = [
            'id', 'customer', 'customer_full_name', 'scheduled_at', 'delivered_at',
            'address_snapshot', 'quantity_liters', 'created_by', 'notes', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'created_by']
