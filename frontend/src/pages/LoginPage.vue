<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex bg-image flex-center">
        <q-card v-bind:style="$q.screen.lt.sm?{'width': '80%'}:{'width':'30%'}">
          <q-card-section>
            <q-avatar size="103px" style="background-color:white" class="absolute-center shadow-10">
              <img src="profile.png" alt="Perfil" style="height: auto; width: 80%">
            </q-avatar>
          </q-card-section>
          <q-card-section>
            <div class="text-center q-pt-lg">
              <div class="col text-h6 ellipsis" style="line-height:1rem; margin-top: 15px;">
                {{ !isFormRecover ? 'INICIAR SESIÓN' : 'RECUPERAR CLAVE'}} <br>
                <span style="font-size: x-small;text-decoration: underline;">smartdoctor</span>
              </div>
            </div>
          </q-card-section>
          <q-card-section>
            <div v-if="!isFormRecover" class="q-gutter-md">
              <q-form @submit="login">
                <q-input filled v-model="username" label="Nombre de usuario" lazy-rules />
                <q-input type="password" filled v-model="password" label="Clave de acceso" lazy-rules class="q-mt-md" />
                <div class="row justify-evenly items-center">
                  <div class="q-mt-md">
                    <q-btn no-caps icon="login" label="Iniciar sesión" type="submit" color="primary"/>
                  </div>
                  <div class="q-mt-md">
                    <q-btn no-caps icon="lock_reset" label="Recuperar mi clave" color="light-blue" @click="isFormRecover = !isFormRecover"/>
                  </div>
                </div>
              </q-form>
            </div>
            <div v-else class="q-gutter-md">
              <q-form @submit="recuperarClave">
                <q-input type="email" filled v-model="email" label="Ingrese su correo" lazy-rules />
                <div class="row q-mt-md">
                  <q-btn no-caps icon="send" label="Enviar correo" color="primary" @click="recuperarClave"/>
                </div>
              </q-form>
            </div>
          </q-card-section>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from 'src/stores/auth'
import { useRoute, useRouter } from 'vue-router'

import { api } from 'src/boot/axios'

const route = useRoute()
const router = useRouter()
const store = useAuthStore()

const username = ref(null)
const password = ref(null)
const email = ref(null)

const isFormRecover = ref(false)

const login = async () => {
  await store.login({ username: username.value, password: password.value })

  if (route.query.redirect) {
    router.push({ path: route.query.redirect })
    return
  }
  router.push({ name: 'users' })
}

const recuperarClave = async () => {
  await api.post('security/users/forgot-password/', { email: email.value })
  isFormRecover.value = false
}
</script>
