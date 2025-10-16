from rest_framework import serializers
from .models import MessageLog


class MessageLogSerializer(serializers.ModelSerializer):
    customer_full_name = serializers.CharField(source='customer.full_name', read_only=True)

    class Meta:
        model = MessageLog
        fields = [
            'id', 'customer', 'customer_full_name', 'provider_message_id',
            'template_name', 'payload', 'status', 'error_detail', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
