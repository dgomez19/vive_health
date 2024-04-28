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


class Patient(TimeStampedModel):
    """
    Representa un paciente en el sistema
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


class Appointment(TimeStampedModel):
    """
    Representa una cita medica en el sistema
    """
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.PROTECT,
        related_name='appointment'
    )

    specialist = models.ForeignKey(
        Specialist,
        on_delete=models.PROTECT,
        related_name='appointment'
    )

    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.PROTECT,
        related_name='appointment'
    )

    date_appointment = models.DateField(
        verbose_name="Fecha cita",
    )

    hour_appointment = models.TimeField(
        verbose_name="Fecha cita",
    )

    class Meta:
        app_label = 'appointment'
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
        default_permissions = ()
        # unique_together = [['specialist', 'date_appointment', 'hour_appointment']]
