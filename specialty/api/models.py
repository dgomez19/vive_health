import uuid

from django.db import models
from model_utils.models import TimeStampedModel

class Specialty(TimeStampedModel):
    """
    Representa una especialidad en el sistema
    """
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    name = models.CharField(
        verbose_name="Name",
        max_length=50
    )
