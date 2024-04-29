import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from model_utils.models import TimeStampedModel
from .managers import UserManager


class User(AbstractUser, TimeStampedModel):
    ROLE_ADMINISTRATOR = 1

    CHOICE_ROLES = (
        (ROLE_ADMINISTRATOR, 'Administrador'),
    )

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.PositiveSmallIntegerField(choices=CHOICE_ROLES)
    email = models.EmailField(unique=True)
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email
