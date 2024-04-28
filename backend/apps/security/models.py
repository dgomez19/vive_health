import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from model_utils.models import TimeStampedModel
from .managers import UserManager
from .utils import random_password


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

    def save(self, *args, **kwargs):
        creating = not self.pk
        super(User, self).save(*args, **kwargs)

        if creating:
            self.generate_new_password()

    def generate_new_password(self):
        password = random_password(6)
        self.set_password(password)
        self.save()
        self.send_access_data(password)

    def send_access_data(self, password):
        subject = 'Smartdoctor - Datos de acceso'
        data = {
            'full_name': self.get_full_name(),
            'username': self.username,
            'password': password,
            'site_url': settings.SITE_URL
        }

        message = render_to_string('emails/generate-password.html', {'data': data})
        self._send_mail(subject, message)

    def _send_mail(self, subject, message):
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.email], html_message=message,
                  fail_silently=False)
