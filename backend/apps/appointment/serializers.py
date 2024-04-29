from rest_framework import serializers

from .models import (
    Specialist,
    Specialty,
    Patient,
    Appointment
)

from .utils import (
    get_work_schedule,
)


class SpecialistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialist
        fields = [
            'uuid',
            'names',
            'surnames',
            'birthdate',
            'address',
            'cell_phone',
            'document',
        ]


class SpecialistAvailableTimesSerializer(serializers.ModelSerializer):

    available_times = serializers.SerializerMethodField()

    class Meta:
        model = Specialist
        fields = [
            'uuid',
            'names',
            'surnames',
            'birthdate',
            'address',
            'cell_phone',
            'document',
            'available_times'
        ]

    def get_available_times(self, obj):
        times_busy = None

        if self.context.get("request").GET.get('date_appointment'):
            times_busy = obj.appointment.filter(
                date_appointment=self.context.get("request").GET.get('date_appointment')
            )

            time_available = get_work_schedule()

            for busy in times_busy:
                posicion = 0

                while posicion < len(time_available):
                    if time_available[posicion] == str(busy.hour_appointment)[0:5]:
                        time_available.pop(posicion)
                    else:
                        posicion += 1

            return time_available

        return []


class PatientCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            'names',
            'surnames',
            'birthdate',
            'address',
            'cell_phone',
            'document',
        ]


class PatientListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Patient
        fields = [
            'uuid',
            'names',
            'surnames',
            'birthdate',
            'address',
            'cell_phone',
            'document',
        ]


class SpecialtySerializer(serializers.ModelSerializer):

    class Meta:
        model = Specialty
        fields = [
            'uuid',
            'name',
        ]


class AppointmentCreateSerializer(serializers.ModelSerializer):

    patient = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Patient.objects.all(),
        required=False,
        allow_null=True
    )

    specialist = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Specialist.objects.all()
    )

    specialty = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Specialty.objects.all()
    )

    class Meta:
        model = Appointment
        fields = [
            'patient',
            'specialist',
            'specialty',
            'date_appointment',
            'hour_appointment',
        ]

    def validate(self, attrs):
        schedule = get_work_schedule()

        if str(attrs.get('hour_appointment'))[0:5] not in schedule:
            raise serializers.ValidationError(
                detail=f"EL HORARIO {str(attrs.get('hour_appointment'))[0:5]} NO SE ENCUENTRA DISPONIBLE."
            )

        appointment = Appointment.objects.filter(
            date_appointment=attrs.get('date_appointment'),
            hour_appointment=attrs.get('hour_appointment'),
            specialist=attrs.get('specialist'),
        ).first()

        if appointment:
            raise serializers.ValidationError(
                detail=f"EL ESPECIALISTA {appointment.specialist.names} YA \
                CUENTA CON UNA CITA PARA LAS FECHAS SELECCIONADAS."
            )

        return attrs


class AppointmentListSerializer(serializers.ModelSerializer):

    patient = PatientListSerializer()

    specialist = SpecialistSerializer()
    specialty = SpecialtySerializer()

    class Meta:
        model = Appointment
        fields = [
            'uuid',
            'patient',
            'specialist',
            'specialty',
            'date_appointment',
            'hour_appointment'
        ]
