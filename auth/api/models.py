import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from model_utils.models import TimeStampedModel

from .managers import UsuarioManager
from .utils import generar_cadena_aleatoria


class Usuario(AbstractUser, TimeStampedModel):
    """
    Representa un Usuario en el sistema
    """
    uuid = models.UUIDField(
        db_index=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )

    first_name = models.CharField(
        'first name',
        max_length=150,
        blank=True
    )

    objects = UsuarioManager()

    def __str__(self):
        """
        Retorna la representación de la instancia del modelo
        """
        return self.email

    def save(self, *args, **kwargs):
        creando = not self.pk
        super(Usuario, self).save(*args, **kwargs)

        if creando:
            self.generar_nueva_clave()

    def generar_nueva_clave(self):
        """
        Genera una nueva contraseña para el usuario
        """
        password = generar_cadena_aleatoria(6)
        print('PASS')
        print(password)
        self.set_password(password)
        self.save()
