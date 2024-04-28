<template>
  <q-layout view="lHh LpR lFf">
    <q-header reveal :class="$q.dark.isActive ? 'header_dark' : 'header_normal'">
      <q-toolbar>
        <q-btn @click="left = !left" flat round dense icon="menu" class="q-mr-sm" />
        <q-toolbar-title>smartdoctor</q-toolbar-title>
        <q-btn class="q-mr-xs" flat round @click="$q.dark.toggle()"
               :icon="$q.dark.isActive ? 'nights_stay' : 'wb_sunny'" />
        <q-btn-dropdown round flat icon="person">
          <div class="row no-wrap q-pa-md">
            <div class="column items-center">
              <q-avatar @click="openModal" size="72px" style="cursor: pointer;">
                <img src="profile.png" alt="profile">
              </q-avatar>
              <div @click="openModal" class="text-subtitle1 q-mt-md q-mb-xs cursor" >{{user.email}}</div>
              <q-btn color="primary" icon="logout" push size="sm" @click="signOff" v-close-popup>
                <q-tooltip>Cerrar sesión</q-tooltip>
              </q-btn>
            </div>
          </div>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer show-if-above v-model="left" side="left" class="text-white drawer_estilo" elevated>
      <div class="full-height" :class="$q.dark.isActive ? 'drawer_dark' : 'drawer_normal'">
        <div style="height: calc(100% - 117px); padding:10px;">
          <q-toolbar>
            <q-avatar>
              <img src="profile.png" alt="profile"/>
            </q-avatar>
            <q-toolbar-title>smartdoctor</q-toolbar-title>
          </q-toolbar>
          <hr />

          <q-scroll-area style="height:100%;">

            <q-list padding>

              <template v-for="(item, i) in items" :key="i + 1">

                <template v-if="item.subitems">
                  <group-navigation v-bind="item" />
                </template>

                <template v-else>
                  <item-navigation v-bind="item" />
                </template>

              </template>

            </q-list>

          </q-scroll-area>

        </div>
      </div>
    </q-drawer>

    <q-dialog v-model="dialog" :position="position" persistent>
      <q-card style="width: 700px; max-width: 80vw;">
        <q-card-section class="row items-center">
          <div class="text-h6">Mi perfil</div>
          <q-space />
          <q-btn icon="close" flat round dense v-close-popup />
        </q-card-section>
        <q-banner class="bg-grey-3">
          <template v-slot:avatar>
            <q-icon name="warning" color="warning" />
          </template>
          Los campos marcados con (*) son obligatorios
        </q-banner>
        <q-form ref="form">
          <q-card-section>
            <div class="row q-col-gutter-sm justify-around">
              <div class="col-5 col-md-5">
                <q-input white dense color="blue" v-model="user.firstName" label="Nombres *" lazy-rules
                         :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']" />
              </div>
              <div class="col-5 col-md-5">
                <q-input white dense color="blue" v-model="user.lastName" label="Apellidos *" lazy-rules
                         :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']" />
              </div>
            </div>
            <div class="row q-col-gutter-sm justify-around">
              <div class="col-11 col-md-11">
                <q-input autocomplete="off" white dense color="blue" v-model="user.email" label="Correo electrónico *"
                         lazy-rules :rules="[ val => val && val.length > 0 || 'El campo es obligatorio']" />
              </div>
            </div>
            <div class="row q-col-gutter-sm justify-around">
              <div v-if="newPassword" class="col-md-5">
                <q-input autocomplete="off" type="password" white dense color="blue" v-model="user.currentPassword"
                         label="Contraseña *" lazy-rules />
              </div>
              <div v-else class="col-md-5">
                <q-input autocomplete="off" type="password" white dense color="blue" v-model="user.currentPassword"
                         label="Contraseña" />
              </div>
              <div class="col-md-5">
                <q-input autocomplete="off" type="password" white dense color="blue" v-model="user.newPassword"
                         lazy-rules :rules="[password]" label="Nueva contraseña" />
              </div>
            </div>
          </q-card-section>
          <q-card-actions align="right" class="bg-white text-teal">
            <q-btn round type="submit" icon="save" @click.prevent="editUser" color="blue-8">
              <q-tooltip>Actualizar datos</q-tooltip>
            </q-btn>
            <q-btn round icon="cancel" v-close-popup color="negative">
              <q-tooltip>Cancelar</q-tooltip>
            </q-btn>
          </q-card-actions>
        </q-form>
      </q-card>
    </q-dialog>

    <q-page-container>
      <q-page class="row no-wrap">
        <div class="col">
          <div class="full-height">
            <q-scroll-area class="col q-pr-sm full-height" visible>
              <router-view />
            </q-scroll-area>
          </div>
        </div>
      </q-page>
    </q-page-container>

  </q-layout>
</template>

<script setup>
import { ref, onMounted, reactive, watch } from 'vue'
import { useQuasar } from 'quasar'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'src/stores/auth'
import { api } from 'boot/axios'

import { USER_MODULE, READ_ACTION } from 'src/constants/permissions'
import { password } from 'src/utils/validations'

import ItemNavigation from 'src/components/ItemNavigation.vue'
import GroupNavigation from 'src/components/GroupNavigation.vue'

const items = [
  {
    icon: 'person',
    title: 'Usuarios',
    route: '/users',
    action: READ_ACTION,
    module: USER_MODULE
  },
  {
    icon: 'personal_injury',
    title: 'Pacientes',
    route: '/patients',
    action: READ_ACTION,
    module: USER_MODULE
  },
  {
    icon: 'person_add',
    title: 'Especialistas',
    route: '/specialist',
    action: READ_ACTION,
    module: USER_MODULE
  },
  {
    icon: 'health_and_safety',
    title: 'Especialidades',
    route: '/specialty',
    action: READ_ACTION,
    module: USER_MODULE
  },
  {
    icon: 'fact_check',
    title: 'Agendar cita',
    route: '/appointment',
    action: READ_ACTION,
    module: USER_MODULE
  }
]

const $q = useQuasar()
const router = useRouter()
const store = useAuthStore()

const left = ref(false)
const dialog = ref(false)
const position = ref('top')
const newPassword = ref(null)
const form = ref(null)
const url = 'security/profile/'

const user = reactive({
  firstName: null,
  lastName: null,
  email: null,
  currentPassword: null,
  newPassword: null
})

const dataUser = () => {
  user.firstName = store.first_name
  user.lastName = store.last_name
  user.email = store.email
}

watch(() => store.uuid, dataUser)

const openModal = () => {
  dialog.value = true
  user.currentPassword = null
  user.newPassword = null
}

const signOff = () => {
  $q.dialog({
    title: 'Confirmación',
    message: '¿Está seguro que desea cerrar sesión?',
    ok: {
      label: 'Si',
      color: 'positive'
    },
    cancel: {
      label: 'No',
      color: 'negative'
    }
  }).onOk(() => {
    store.logout()
    router.push({ name: 'login' })
  })
}

const editUser = () => {
  form.value.validate().then(async (success) => {
    if (success) {
      api.put(url, {
        first_name: user.firstName,
        last_name: user.lastName,
        email: user.email,
        current_password: user.currentPassword,
        new_password: user.newPassword
      }).then(() => {
        store.update({
          first_name: user.firstName,
          last_name: user.lastName,
          email: user.email
        })
        dialog.value = false
        dataUser()
      })
    }
  })
}

onMounted(() => {
  dataUser()
})
</script>

<style lang="scss">
.q-drawer {
  background-size: cover !important;
}

.drawer_normal {
  background-color: rgba(1, 1, 1, 0.75);
}

.drawer_dark {
  background-color: #010101f2;
}

.body--light {
  background: #f1f1f1 !important;
}

body.body--dark {
  background: #000
}

.header_normal {
  background: linear-gradient(
    145deg,
    #025ba9,
    #025ba9
  );
}

.header_dark {
  background: linear-gradient(145deg, rgb(61, 14, 42) 15%, rgb(14, 43, 78) 70%);
}
.drawer_estilo {
  background-image: linear-gradient(135deg, rgb(2, 91, 169) 0%,
  rgb(255 255 255 / 60%) 100%) !important;
}
</style>
