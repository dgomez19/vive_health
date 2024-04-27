import uuid

from django.db import models
from model_utils.models import TimeStampedModel


class Specialist(TimeStampedModel):
    pass


class Appointment(TimeStampedModel):
    """
    Representa una cita en el sistema
    """
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        related_name='appointment'
    )
