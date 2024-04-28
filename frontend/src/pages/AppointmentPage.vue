<template>
  <q-page>
    <q-dialog ref="dialog" persistent>
      <q-card flat bordered class="q-pa-md" style="width: 1080px; max-width: 80vw;">

        <q-card-section horizontal class="row items-center q-mb-md">
          <q-icon name="personal_injury" size="sm" class="q-mx-md"/>
          <div class="text-h6">AGENDAR CITA</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>

        <q-banner class="bg-grey-3">
          <template v-slot:avatar>
            <q-icon name="warning" color="warning" />
          </template>
          Los campos marcados con (*) son obligatorios
        </q-banner> <br>

        <q-form ref="form" @submit="submit" @reset="reset">
          <div class="row">
            <div class="col-5 col-md-5 col-xs-12">
              <q-select clearable use-input input-debounce="0" v-model="patient" label="Paciente *" :options="patients" option-label="names" option-value="uuid" lazy-rules :rules="[obligatorio]" />
            </div>

            <div class="col-1 col-md-1 col-xs-12">
              &nbsp;
            </div>

            <div class="col-5 col-md-5 col-xs-12">
              <q-select clearable use-input input-debounce="0" v-model="specialist" label="Especialista *" :options="specialists" option-label="names" option-value="uuid" lazy-rules :rules="[obligatorio]" />
            </div>
          </div>

          <div class="row">
            <div class="col-5 col-md-5 col-xs-12">
              <q-select clearable use-input input-debounce="0" v-model="specialty" label="Especialidad *" :options="specialties" option-label="name" option-value="uuid" lazy-rules :rules="[obligatorio]" />
            </div>

            <div class="col-1 col-md-1 col-xs-12">
              &nbsp;
            </div>

            <div class="col-5 col-md-5 col-xs-12">
              <q-input v-model="dateAppointment" mask="####-##-##" label="Fecha cita *" lazy-rules :rules="[obligatorio, validarFecha('YYYY-MM-DD')]">
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy ref="qDateProxy" cover transition-show="scale" transition-hide="scale">
                      <q-date
                        v-model="dateAppointment"
                      >
                        <div class="row items-center justify-end">
                          <q-btn v-close-popup label="Cerrar" color="primary" flat />
                        </div>
                      </q-date>
                    </q-popup-proxy>
                  </q-icon>
                </template>
              </q-input>
            </div>
          </div>

          <div class="row">
            <div class="col-5 col-md-5 col-xs-12">
              <q-select clearable use-input input-debounce="0" v-model="hourAppointment" label="Horarios disponibles *" :options="hours" lazy-rules :rules="[obligatorio]" />
            </div>
          </div>

          <div class="row justify-right">
            <q-card-actions class="bg-white text-teal">
              <q-btn v-if="!isEditing" round icon="save" @click.prevent="submit" type="submit" color="primary"/>
            </q-card-actions>
          </div>
        </q-form>
      </q-card>
    </q-dialog>

    <div class="q-pa-md">

      <q-card class="card">
        <q-card-section>
          <div>Filtros</div>
            <q-form ref="buscarFormulario" @submit="load({ pagination: pagination })">
              <div class="q-pa-sm">
                <div class="row">
                  <div class="col-3 col-md-3 col-xs-3">
                    <q-select clearable use-input input-debounce="0" v-model="filters.patient" label="Paciente *" :options="patients" option-label="names" option-value="uuid" />
                  </div>

                  <div class="col-1 col-md-1 col-xs-12">
                    &nbsp;
                  </div>

                  <div class="col-3 col-md-3 col-xs-3">
                    <q-select clearable use-input input-debounce="0" v-model="filters.specialist" label="Especialista *" :options="specialists" option-label="names" option-value="uuid" />
                  </div>

                  <div class="col-1 col-md-1 col-xs-12">
                    &nbsp;
                  </div>

                  <div class="col-3 col-md-3 col-xs-3">
                    <q-select clearable use-input input-debounce="0" v-model="filters.specialty" label="Especialidad *" :options="specialties" option-label="name" option-value="uuid" />
                  </div>
                </div> <br>

                <div class="row">
                  <div class="col-1 col-md-1 col-xs-1">
                    <q-btn round icon="search" type="submit" color="primary"/>
                  </div>
                </div>

              </div>
            </q-form>
        </q-card-section>
      </q-card>

      <q-table
        flat
        bordered
        virtual-scroll
        color="primary"
        class=""
        :loading="loading"
        :columns="columns"
        :rows="appointmentList"
        row-key="name"
        :rows-per-page-options="[10]"
        :filter="filtro"
        @request="load"
      >
        <template #top>
          <q-btn push rounded rippe no-caps size="md" label="AGENDAR CITA" color="primary" icon="add" @click="openAdd"/>
          <q-space />
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props">
            <q-btn round size="xs" color="negative" icon="delete_forever" v-on:click="onDelete(props.row.uuid)" />
          </q-td>
        </template>

        <template v-slot:no-data>
          <div class="full-width row flex-center text-red">
            <q-icon name="search_off" size="25px"/>
            <span class="q-ml-sm">
              No se encontraron {{titulo}} para listar
            </span>
          </div>
        </template>
      </q-table>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'

import { api } from 'boot/axios'

import { obligatorio, validarFecha } from 'src/utils/validations'

import { useQuasar } from 'quasar'

import moment from 'moment'

import Swal from 'sweetalert2'

const columns = [
  { name: 'patient', sortable: true, label: 'PACIENTE', align: 'center', field: 'patient', format: row => `${row.names} ${row.surnames} (${row.document})` },
  { name: 'specialist', label: 'ESPECIALISTA', align: 'center', field: 'specialist', format: row => `${row.names} ${row.surnames}` },
  { name: 'specialty', label: 'Especialidad', align: 'center', field: 'specialty', format: row => row.name },
  { name: 'date_appointment', label: 'Fecha cita', align: 'center', field: 'date_appointment' },
  { name: 'hour_appointment', label: 'Hora cita', align: 'center', field: 'hour_appointment' },
  { name: 'actions', label: 'Acciones', align: 'center', field: 'actions' }
]

const pagination = ref({
  page: 1,
  rowsPerPage: 100,
  rowsNumber: 10,
  sortBy: 'created',
  descending: true,
  allRows: 100
})

const appointmentList = ref([])
const dialog = ref(false)
const patient = ref(null)
const dateAppointment = ref(null)
const hourAppointment = ref(null)

const patients = ref([])

const specialty = ref(null)
const specialties = ref([])

const specialist = ref(null)
const specialists = ref([])
const hours = ref([])

const filters = ref({
  patient: null,
  specialist: null,
  specialty: null
})

const isEditing = ref(false)

const form = ref(null)
const $q = useQuasar()

const load = async (props) => {
  const documentUuid = filters.value.patient !== null ? filters.value.patient.uuid : ''

  const specialistUuid = filters.value.specialist !== null ? filters.value.specialist.uuid : ''

  const specialtyUuid = filters.value.specialty !== null ? filters.value.specialty.uuid : ''

  const params = new URLSearchParams({
    page: props.pagination.page,
    size: props.pagination.rowsPerPage,
    patient__uuid: documentUuid,
    specialist__uuid: specialistUuid,
    specialty__uuid: specialtyUuid
  })

  try {
    const { data } = await api.get(`appointment/?${params}`)
    appointmentList.value = data.data
    pagination.value = { ...props.pagination, rowsNumber: data.cantidad }
  } catch (err) {}
}

const openAdd = async (props) => {
  reset()
  dialog.value.show()
  isEditing.value = false
}

const reset = () => {
  patient.value = null
  specialist.value = null
  specialty.value = null
  dateAppointment.value = null
  hourAppointment.value = null
}

const submit = async () => {
  const isValid = await form.value.validate()

  if (!isValid) return

  try {
    await api.post('appointment/', {
      patient: patient.value.uuid,
      specialist: specialist.value.uuid,
      specialty: specialty.value.uuid,
      date_appointment: dateAppointment.value,
      hour_appointment: hourAppointment.value
    })

    await load({ pagination: pagination.value })
    dialog.value.hide()
  } catch (err) {}
}

const onDelete = async (uuid) => {
  $q.dialog({
    title: 'Confirmación',
    message: 'Desea eliminar el registro?',
    ok: {
      label: 'Si',
      color: 'positive'
    },
    cancel: {
      label: 'No',
      color: 'negative'
    }
  }).onOk(() => {
    api.delete('appointment/' + uuid + '/').then(_response => {
      load({ pagination: pagination.value })
    })
  })
}

const loadPatients = async () => {
  const { data } = await api.get('appointment/patient/')
  patients.value = data
}

const loadSpecialists = async () => {
  const { data } = await api.get('appointment/specialist/')
  specialists.value = data
}

const loadSpecialties = async () => {
  const { data } = await api.get('appointment/specialty/')
  specialties.value = data
}

watch(dateAppointment, async (value) => {
  if (!specialist.value) {
    Swal.fire({
      customClass: { container: 'my-swal' },
      title: '<strong>ATENCIÓN</strong>',
      icon: 'error',
      html: 'DEBE SELECCIONAR UN ESPECIALISTA PARA CONOCER SUS HORARIOS DISPONIBLES.',
      showCloseButton: true,
      focusConfirm: false,
      confirmButtonText: 'Aceptar'
    })

    return false
  }

  const date = moment(String(value)).format('YYYY-MM-DD')
  const { data } = await api.get(`appointment/available-times/?date_appointment=${date}&specialist=${specialist.value.uuid}`)
  if (data[0]) {
    hours.value = data[0].available_times
  }
})

onMounted(async () => {
  await load({ pagination: pagination.value })
  await loadPatients()
  await loadSpecialists()
  await loadSpecialties()
})

</script>
