<template>
  <q-page>
    <q-dialog ref="dialog" persistent>
      <q-card flat bordered class="q-pa-md" style="width: 1080px; max-width: 80vw;">

        <q-card-section horizontal class="row items-center q-mb-md">
          <q-icon name="personal_injury" size="sm" class="q-mx-md"/>
          <div class="text-h6">AGREGAR ESPECIALISTAS</div>
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
              <q-input outlined v-model="document" label="Documento *" hint="Ingrese el número de documento del especialista" lazy-rules :rules="[obligatorio]" />
            </div>
          </div>

          <div class="row justify-around">
            <div class="col-5 col-md-5 col-xs-12">
              <q-input outlined v-model="names" label="Nombres *" lazy-rules :rules="[obligatorio]" />
            </div>

            <div class="col-2 col-md-2 col-xs-12">
              &nbsp;
            </div>

            <div class="col-5 col-md-5 col-xs-12">
              <q-input outlined v-model="surnames" label="Apellidos *" lazy-rules :rules="[obligatorio]" />
            </div>
          </div>

          <div class="row justify-around">
            <div class="col-5 col-md-5 col-xs-12">
              <q-input outlined v-model="cellPhone" label="Número Celular *" lazy-rules :rules="[obligatorio]" />
            </div>

            <div class="col-2 col-md-2 col-xs-12">
              &nbsp;
            </div>

            <div class="col-5 col-md-5 col-xs-12">
              <q-input v-model="birthdate" mask="####-##-##" label="Fecha nacimiento *" lazy-rules :rules="[obligatorio, validarFecha('YYYY-MM-DD')]">
                <template v-slot:append>
                  <q-icon name="event" class="cursor-pointer">
                    <q-popup-proxy ref="qDateProxy" cover transition-show="scale" transition-hide="scale">
                      <q-date
                        v-model="birthdate"
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

          <div class="row justify-around">
            <div class="col-12 col-md-12 col-xs-12">
              <q-input outlined v-model="address" label="Dirección *" lazy-rules :rules="[obligatorio]" />
            </div>
          </div>

          <div class="row justify-right">
            <q-card-actions class="bg-white text-teal">
              <q-btn v-if="!isEditing" round icon="save" @click.prevent="submit" type="submit" color="primary"/>
              <q-btn v-else round icon="save" @click.prevent="update" type="submit" color="primary"/>
            </q-card-actions>
          </div>
        </q-form>
      </q-card>
    </q-dialog>

    <div class="q-pa-md">
      <q-table
        flat
        bordered
        virtual-scroll
        color="primary"
        class=""
        :loading="loading"
        :columns="columns"
        :rows="dataList"
        row-key="name"
        :rows-per-page-options="[10]"
        :filter="filtro"
      >
        <template #top>
          <q-btn push rounded rippe no-caps size="md" label="Agregar especialista" color="primary" icon="add" @click="openAdd"/>
          <q-space />
        </template>

        <template #body-cell-actions="props">
          <q-td :props="props">
            <q-btn round size="xs" color="primary" icon="edit" v-on:click="editing(props.row)" /> &nbsp;
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
import { ref, onMounted } from 'vue'

import { api } from 'boot/axios'

import { validarFecha, obligatorio } from 'src/utils/validations'

import moment from 'moment'

import { useQuasar } from 'quasar'

const columns = [
  { name: 'document', label: 'Documento', align: 'center', field: 'document' },
  { name: 'names', label: 'Nombres', align: 'center', field: 'names' },
  { name: 'surnames', label: 'Apellidos', align: 'center', field: 'surnames' },
  { name: 'address', label: 'Dirección', align: 'center', field: 'address' },
  { name: 'cell_phone', label: 'Celular', align: 'center', field: 'cell_phone' },
  { name: 'actions', label: 'Acciones', align: 'center', field: 'actions' }
]

const pagination = ref({
  page: 1,
  rowsPerPage: 100,
  rowsNumber: 0,
  sortBy: 'created',
  descending: true,
  allRows: 100
})

const dataList = ref([])
const dialog = ref(false)
const document = ref(null)
const names = ref(null)
const surnames = ref(null)
const cellPhone = ref(null)
const birthdate = ref(null)
const address = ref(null)
const uuid = ref(null)

const isEditing = ref(false)

const form = ref(null)
const $q = useQuasar()

const load = async (props) => {
  const params = new URLSearchParams({
    page: props.pagination.page,
    size: props.pagination.rowsPerPage
  })

  try {
    const { data } = await api.get(`appointment/specialist/?${params}`)
    dataList.value = data.data
    pagination.value = { ...props.pagination, rowsNumber: data.cantidad }
  } catch (err) {}
}

const openAdd = async (props) => {
  reset()
  dialog.value.show()
  isEditing.value = false
}

const reset = () => {
  document.value = null
  names.value = null
  surnames.value = null
  cellPhone.value = null
  birthdate.value = null
  address.value = null
  uuid.value = null
}

const submit = async () => {
  const isValid = await form.value.validate()

  if (!isValid) return

  try {
    await api.post('appointment/specialist/', {
      document: document.value,
      names: names.value,
      surnames: surnames.value,
      cell_phone: cellPhone.value,
      address: address.value,
      birthdate: moment(String(birthdate.value)).format('YYYY-MM-DD')
    })

    await load({ pagination: pagination.value })
    dialog.value.hide()
  } catch (err) {}
}

const update = async () => {
  const isValid = await form.value.validate()

  if (!isValid) return

  try {
    await api.put(`appointment/specialist/${uuid.value}/`, {
      document: document.value,
      names: names.value,
      surnames: surnames.value,
      cell_phone: cellPhone.value,
      address: address.value,
      birthdate: moment(String(birthdate.value)).format('YYYY-MM-DD')
    })

    await load({ pagination: pagination.value })
    dialog.value.hide()
  } catch (err) {}
}

const editing = async (data) => {
  reset()
  dialog.value.show()

  isEditing.value = true
  document.value = data.document
  names.value = data.names
  surnames.value = data.surnames
  cellPhone.value = data.cell_phone
  address.value = data.address
  birthdate.value = data.birthdate
  uuid.value = data.uuid
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
    api.delete('appointment/specialist/' + uuid + '/').then(_response => {
      load({ pagination: pagination.value })
    })
  })
}

onMounted(async () => {
  await load({ pagination: pagination.value })
})

</script>
