from django.contrib import admin
from .models import MessageLog


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
    list_display = ("customer", "template_name", "status", "created_at")
    list_filter = ("status", "template_name")
    search_fields = ("customer__full_name", "provider_message_id")

# Register your models here.
