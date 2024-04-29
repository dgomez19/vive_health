
from rest_framework.test import APITestCase

from rest_framework import status

from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory

from django.contrib.auth.models import User

from apps.security.models import User

from apps.appointment.models import Patient, Specialist, Specialty, Appointment

from django.contrib.auth.hashers import make_password


class MyModelAPITest(APITestCase):

    url = '/api/v1/appointment/patient/'

    def setUp(self):
        user = User.objects.create(
            username='test',
            password=make_password('test'),
            first_name='test',
            last_name='test',
            email="test@test.com",
            role=1
        )

        self.client.force_authenticate(user=user)

    def test_create_patient(self):
        """
        can create a new PATIENT object.
        """
        data = {
            'names': 'pruebas',
            'surnames': 'pruebas2024',
            'birthdate': '1980-02-01',
            'address': 'CALI - COLOMBIA',
            'cell_phone': '31313',
            'document': '129309123'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_birthdate_error(self):
        """
        Error al crear paciente por fecha de nacimiento
        con formato incorrecto
        """
        data = {
            'names': 'pruebas',
            'surnames': 'pruebas2024',
            'birthdate': 'YYYY-MM-DD',
            'address': 'MEDELLIN - COLOMBIA',
            'cell_phone': '31313',
            'document': '129309123'
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_fields_obligatories(self):
        """
        Error al crear paciente por campos obligatorios vacios
        """
        data = {
            'names': '',
            'surnames': '',
            'birthdate': '1980-02-01',
            'address': 'ITAGUI - COLOMBIA',
            'cell_phone': '',
            'document': ''
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_fields_max_length(self):
        """
        Error al crear paciente por campos obligatorios vacios
        """
        text_length = f'ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ \
            ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ \
            ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ'

        data = {
            'names': text_length,
            'surnames': text_length,
            'birthdate': text_length,
            'address': text_length,
            'cell_phone': text_length,
            'document': text_length
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_update_patient(self):
        """
        Actualizar la informacion del paciente
        """
        patient = Patient.objects.create(
            names='pruebas',
            surnames='pruebas2024',
            birthdate='1980-02-01',
            address='ITAGUI - COLOMBIA',
            cell_phone='31313',
            document='129309123'
        )

        url = f'{self.url}{patient.uuid}'

        data = {
            'names': 'pruebas2',
            'surnames': 'pruebas2024',
            'birthdate': '1980-02-01',
            'address': 'ITAGUI - COLOMBIA',
            'cell_phone': '31313',
            'document': '129309123'
        }

        response = self.client.put(url, data, follow=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_patient_non_existent(self):
        """
        Intenta actualizar un paciente inexistente
        """
        url = f'{self.url}non-existent/'

        response = self.client.put(url, {}, follow=True)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



    def test_appointment_create(self):
        """
        Agendar una cita medica
        """
        patient = self.create_patient('1')
        specialist = self.create_specialist('2')
        specialty = self.create_specialty()

        url = '/api/v1/appointment/'

        data = {
            'patient': patient.uuid,
            'specialist': specialist.uuid,
            'specialty': specialty.uuid,
            'date_appointment': '2024-01-01',
            'hour_appointment': '08:00'
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_appointment_busy(self):
        """
        Agendar una cita medica, en un horario existente
        """
        self.create_appointment()

        url = '/api/v1/appointment/'

        exist_appointment = Appointment.objects.filter().first()

        data = {
            'patient': exist_appointment.patient.uuid,
            'specialist': exist_appointment.specialist.uuid,
            'specialty': exist_appointment.specialty.uuid,
            'date_appointment': exist_appointment.date_appointment,
            'hour_appointment': exist_appointment.hour_appointment
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def create_appointment(self):
        patient = self.create_patient('5')
        specialist = self.create_specialist('6')
        specialty = self.create_specialty()

        Appointment.objects.create(
            patient=patient,
            specialist=specialist,
            specialty=specialty,
            date_appointment='2024-01-01',
            hour_appointment='08:00'
        )

    def create_patient(self, document):
        patient = Patient.objects.create(
            names='pruebas',
            surnames='pruebas2024',
            birthdate='1980-02-01',
            address='SOACHA - COLOMBIA',
            cell_phone='31313',
            document=document
        )

        return patient


    def create_specialist(self, document):
        specialist = Specialist.objects.create(
            names='pruebas',
            surnames='pruebas2024',
            birthdate='1980-02-01',
            address='PEREIRA - COLOMBIA',
            cell_phone='31313',
            document=document
        )

        return specialist


    def create_specialty(self):
        specialty = Specialty.objects.create(
            name='pruebas'
        )

        return specialty
