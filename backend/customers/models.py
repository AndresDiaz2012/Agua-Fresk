from django.db import models
from phonenumbers import parse as parse_phone, is_valid_number, format_number, PhoneNumberFormat


class Customer(models.Model):
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)
    phone_e164 = models.CharField(max_length=20, unique=True)
    is_active = models.BooleanField(default=True)
    last_dispatch_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self) -> str:
        return f"{self.full_name} ({self.phone_e164})"

    @staticmethod
    def normalize_phone(raw_phone: str, default_region: str = "MX") -> str:
        pn = parse_phone(raw_phone, default_region)
        if not is_valid_number(pn):
            raise ValueError("Invalid phone number")
        return format_number(pn, PhoneNumberFormat.E164)


# Create your models here.
