<template>
  <q-page>
    <q-dialog ref="dialog" persistent>
      <q-card flat bordered class="q-pa-md" style="width: 1080px; max-width: 80vw;">

        <q-card-section horizontal class="row items-center q-mb-md">
          <q-icon name="personal_injury" size="sm" class="q-mx-md"/>
          <div class="text-h6">AGREGAR ESPECIALIDAD</div>
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
              <q-input outlined v-model="name" label="Nombre especialidad *" lazy-rules :rules="[obligatorio]" />
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
        :rows="patientList"
        row-key="name"
        :rows-per-page-options="[10]"
        :filter="filtro"
      >
        <template #top>
          <q-btn push rounded rippe no-caps size="md" label="Agregar especialidad" color="primary" icon="add" @click="openAdd"/>
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

import { obligatorio } from 'src/utils/validations'

import { useQuasar } from 'quasar'

const columns = [
  { name: 'name', label: 'Nombres', align: 'center', field: 'name' },
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

const patientList = ref([])
const dialog = ref(false)
const name = ref(null)
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
    const { data } = await api.get(`appointment/specialty/?${params}`)
    patientList.value = data.data
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
  name.value = null
  uuid.value = null
}

const submit = async () => {
  const isValid = await form.value.validate()

  if (!isValid) return

  try {
    await api.post('appointment/specialty/', {
      document: document.value,
      name: name.value
    })

    await load({ pagination: pagination.value })
    dialog.value.hide()
  } catch (err) {}
}

const update = async () => {
  const isValid = await form.value.validate()

  if (!isValid) return

  try {
    await api.put(`appointment/specialty/${uuid.value}/`, {
      document: document.value,
      name: name.value
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
  name.value = data.name
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
    api.delete('appointment/specialty/' + uuid + '/').then(_response => {
      load({ pagination: pagination.value })
    })
  })
}

onMounted(async () => {
  await load({ pagination: pagination.value })
})

</script>
