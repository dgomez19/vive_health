import uuid

from django.db import models
from model_utils.models import TimeStampedModel

class Specialist(TimeStampedModel):
    """
    Representa un especialista en el sistema
    """
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    names = models.CharField(
        verbose_name="Names",
        max_length=50
    )

    surnames = models.CharField(
        verbose_name="Surnames",
        max_length=50
    )

    birthdate = models.DateField(
        verbose_name="Birthdate"
    )

    address = models.CharField(
        verbose_name="Address",
        max_length=250
    )

    cell_phone = models.CharField(
        verbose_name="Cell phone",
        max_length=20
    )

    document = models.CharField(
        unique=True,
        verbose_name="Document",
        max_length=50
    )

    def build_filters(self):

        specialists = Specialist.objects.all()

        if self.get('names'):
            specialists = Specialist.objects.filter(names__contains=self.get('names'))

        if self.get('surnames'):
            specialists = Specialist.objects.filter(surnames__contains=self.get('surnames'))

        if self.get('document'):
            specialists = Specialist.objects.filter(document__contains=self.get('document'))

        return specialists
