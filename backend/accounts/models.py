from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_OPERATOR = 'operator'

    ROLE_CHOICES = (
        (ROLE_ADMIN, 'Administrador'),
        (ROLE_OPERATOR, 'Operador'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_OPERATOR)

    def is_admin(self) -> bool:
        return self.role == self.ROLE_ADMIN or self.is_superuser


# Create your models here.
