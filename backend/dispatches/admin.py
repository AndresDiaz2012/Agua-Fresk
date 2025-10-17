from django.contrib import admin
from .models import Dispatch


@admin.register(Dispatch)
class DispatchAdmin(admin.ModelAdmin):
    list_display = ("customer", "scheduled_at", "delivered_at", "quantity_liters")
    list_filter = ("delivered_at",)
    search_fields = ("customer__full_name", "address_snapshot")

# Register your models here.
