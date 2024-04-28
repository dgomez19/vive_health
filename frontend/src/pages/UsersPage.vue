<template>
  <q-page class="q-pa-sm">
    <q-btn unelevated round icon="add" color="primary" @click="create">
      <q-tooltip>Agregar usuarios</q-tooltip>
    </q-btn>
    <q-card class="card q-mt-md">
      <q-linear-progress :value="10" color="blue" />
      <q-card-section>
        <div style="font-size: small;color: #015ca9;">Filtros de búsqueda</div>
        <q-form class="q-gutter-md" @submit.prevent="">
          <div class="row q-col-gutter-sm">
            <div class="col-3 col-md-3 col-xs-6">
              <q-input white color="blue" dense v-model="filters.username" label="Usuario" />
            </div>
            <div class="col-3 col-md-3 col-xs-6">
              <q-input white color="blue" dense v-model="filters.first_name" label="Nombres" />
            </div>
            <div class="col-3 col-md-3 col-xs-6">
              <q-input white color="blue" dense v-model="filters.last_name" label="Apellidos" />
            </div>
            <div class="col-3 col-md-3 col-xs-6">
              <q-input white color="blue" dense v-model="filters.email" label="Correo" />
            </div>
          </div>
          <div class="row q-col-gutter-sm">
            <div class="col-12 col-md-12" style="text-align:right;">
              <q-btn round @click.prevent="getUsers" icon="search" color="primary" type="submit">
                <q-tooltip>Consultar</q-tooltip>
              </q-btn>
            </div>
          </div>
        </q-form>
      </q-card-section>
    </q-card>
    <div class="row q-col-gutter-lg q-mt-xs">
      <div class="col-lg-4 col-md-4 col-xs-12 col-sm-12" v-for="(data, index) in paginationUsers" :key="index">
        <q-card>
          <q-item>
            <q-item-section>
              <q-item-label class="text-grey-8 text-weight-bold">{{ data.username }}</q-item-label>
              <q-item-label caption>
                {{ data.first_name }}
                {{ data.last_name }}
              </q-item-label>
              <q-item-label class="text-grey-8">
                {{ data.email }}
              </q-item-label>
            </q-item-section>
            <q-item-section side>
              <q-item-label>
                <q-btn size="sm" unelevated round icon="login" color="primary" :disable="store.uuid === data.uuid" @click="switchSession(data)" title="Cambiar Sesión" />
              </q-item-label>
              <q-item-label>
                <q-btn size="sm" flat round icon="edit" class="bg-indigo-7 text-white" :disable="store.uuid === data.uuid" @click="edit(data)" />
              </q-item-label>
              <q-item-label>
                <q-btn size="sm" flat round icon="delete_sweep" class="bg-info text-white"
                       style="background-color:#d82626 !important;" :disable="store.uuid === data.uuid" v-on:click="remove(data.uuid)" />
              </q-item-label>
            </q-item-section>
          </q-item>
          <q-separator></q-separator>
          <q-card-section>
            <div class="q-pa-sm text-grey-8">
              Usuario creado el día: {{data.created}}
            </div>
          </q-card-section>
        </q-card>
      </div>
    </div>
    <q-card-actions align="center">
      <q-pagination
        v-model="page"
        :min="currentPage"
        :max="Math.ceil(countItems/totalPages)"
        :input="true"
        input-class="text-orange-10"
        @click="getUsers"
      >
      </q-pagination>
    </q-card-actions>
    <q-dialog v-model="dialog" :position="position" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-linear-progress :value="10" color="blue" />
        <q-card-section class="row items-center">
          <div class="text-h6"> {{ titleModal }} </div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-banner class="bg-grey-3">
          <template v-slot:avatar>
            <q-icon name="warning" color="warning" />
          </template>
          Los campos marcados con (*) son obligatorios
        </q-banner>
        <q-card-section>
          <q-form ref="form" @submit.prevent="">
            <div class="row justify-around">
              <div class="col-md-5">
                <q-input white color="blue" dense v-model="username" label="Usuario *" lazy-rules
                  :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']" />
              </div>
              <div class="col-md-5">
                <q-input white color="blue" dense v-model="firstName" label="Nombres *" lazy-rules
                  :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']" />
              </div>
            </div>
            <div class="row justify-around">
              <div class="col-md-5">
                <q-input white color="blue" dense v-model="lastName" label="Apellidos *"
                  lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']" />
              </div>
              <div class="col-md-5">
                <q-input white color="blue" dense v-model="email" label="Correo electrónico *"
                  lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']" />
              </div>
              <div class="col-md-5">
                <field-selection v-model="role" label="Rol *" url="security/users/roles/" :rules="[ val => !!val || 'El campo es obligatorio']" />
              </div>
              <div class="col-md-5"></div>
            </div>
          </q-form>
        </q-card-section>
        <div class="row justify-between">
          <q-card-actions align="left" class="bg-white text-teal">
            <q-btn v-if="isEditing" round @click.prevent="sendPassword" icon="send" color="info" />
            <q-tooltip>Enviar contraseña</q-tooltip>
          </q-card-actions>
          <q-card-actions align="right" class="bg-white text-teal">
            <div v-if="!isEditing">
              <q-btn round icon="save" @click.prevent="save" color="primary"/>
              <q-tooltip>Guardar datos</q-tooltip>
            </div>
            <div v-else>
              <q-btn round icon="save" @click.prevent="editForm" color="primary"/>
              <q-tooltip>Editar datos</q-tooltip>
            </div>
            <div class="q-ml-xs">
              <q-btn round icon="cancel" v-close-popup color="negative"/>
              <q-tooltip>Cancelar</q-tooltip>
            </div>
          </q-card-actions>
        </div>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'src/stores/auth'
import { useRoute, useRouter } from 'vue-router'
import { api } from 'src/boot/axios'

import FieldSelection from 'src/components/FieldSelection.vue'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const dialog = ref(false)
const position = ref('top')
const page = ref(1)
const currentPage = ref(1)
const totalPages = ref(10)
const countItems = ref(null)
const users = ref([])
const paginationUsers = ref([])
const isEditing = ref(null)
const titleModal = ref(null)
const username = ref(null)
const firstName = ref(null)
const lastName = ref(null)
const email = ref(null)
const role = ref(null)
const form = ref(null)
const uuid = ref(null)
const $q = useQuasar()
const filters = ref([])
const filtersArg = ref('')

const setFilters = () => {
  let filtersSearch = '?page=' + page.value + '&size=' + totalPages.value

  if (filters.value.username) {
    filtersSearch += '&username=' + filters.value.username
  }

  if (filters.value.first_name) {
    filtersSearch += '&first_name=' + filters.value.first_name
  }

  if (filters.value.last_name) {
    filtersSearch += '&last_name=' + filters.value.last_name
  }

  if (filters.value.email) {
    filtersSearch += '&email=' + filters.value.email
  }

  return filtersSearch
}

const pagination = async () => {
  const list = await listUsers()
  paginationUsers.value = list.slice(0, totalPages.value)
}

const listUsers = async () => {
  if (Object.keys(users.value).length > 0) {
    countItems.value = users.value.count
    return users.value.data.filter(function (item) {
      return item
    })
  }

  return []
}

const getUsers = async () => {
  filtersArg.value = setFilters()
  const { data } = await api.get(`security/users/${filtersArg.value}`)
  users.value = data
  pagination()
}

onMounted(async () => {
  await getUsers()
})

const create = () => {
  isEditing.value = false
  clear()
  dialog.value = true
  titleModal.value = 'Agregar usuario'
}

const save = () => {
  form.value.validate().then(async success => {
    if (success) {
      api.post('security/users/', {
        username: username.value,
        first_name: firstName.value,
        last_name: lastName.value,
        email: email.value,
        role: role.value.code
      }).then(() => {
        dialog.value = false
        getUsers()
      })
    }
  })
}

const clear = () => {
  username.value = null
  firstName.value = null
  lastName.value = null
  email.value = null
  role.value = null
}

const switchSession = async (row) => {
  await store.switchSession({ uuid: row.uuid })

  if (route.query.redirect) {
    router.push({ path: route.query.redirect })
    return
  }
  router.push({ name: 'users' })
}

const remove = (uuidUser) => {
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
    api.delete('security/users/' + uuidUser + '/').then(_response => {
      dialog.value = false
      getUsers()
    })
  })
}

const editForm = () => {
  form.value.validate().then(async success => {
    if (success) {
      api.put('security/users/' + uuid.value + '/', {
        username: username.value,
        first_name: firstName.value,
        last_name: lastName.value,
        email: email.value,
        role: role.value.code
      }).then(() => {
        dialog.value = false
        getUsers()
      })
    }
  })
}

const sendPassword = () => {
  api.get('security/users/generate-password/' + uuid.value + '/').then(() => {
    dialog.value = false
    getUsers()
  })
}

const edit = (data) => {
  clear()
  titleModal.value = 'Editar usuario'
  position.value = 'top'
  dialog.value = true
  username.value = data.username
  firstName.value = data.first_name
  lastName.value = data.last_name
  email.value = data.email
  uuid.value = data.uuid
  role.value = data.role
  isEditing.value = true
}
</script>
