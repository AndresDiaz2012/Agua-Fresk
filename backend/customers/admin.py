from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_e164", "is_active", "last_dispatch_date")
    search_fields = ("full_name", "phone_e164", "address")
    list_filter = ("is_active",)


# Register your models here.
