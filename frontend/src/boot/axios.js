import { boot } from 'quasar/wrappers'
import axios from 'axios'
import Swal from 'sweetalert2'
import {
  Loading,
  QSpinnerBall
} from 'quasar'

import { useAuthStore } from 'src/stores/auth'

axios.defaults.baseURL = process.env.API // is obtained from quasar.conf.js
const api = axios.create({ baseURL: process.env.API })

const dispararError = (title, message) => {
  Swal.fire({
    customClass: { container: 'my-swal' },
    title: `<strong>${title}</strong>`,
    icon: 'error',
    html: message,
    showCloseButton: true,
    focusConfirm: false,
    confirmButtonText: 'Aceptar'
  })
}

export default boot(({ app, router, urlPath }) => {
  api.defaults.withCredentials = true
  api.defaults.headers.post['Content-Type'] = 'multipart/form-data'

  api.interceptors.request.use((config) => {
    const store = useAuthStore()

    Loading.show({ spinner: QSpinnerBall })
    config.headers.authorization = `JWT ${store.token}`
    return config
  })

  api.interceptors.response.use((response) => {
    Loading.hide()
    const methodsMessages = ['post', 'put', 'delete']

    if (response.config.url === 'security/login/') {
      Loading.hide()
    } else if (methodsMessages.includes(response.config.method) || response.config.url.includes('security/users/generate-password/')) {
      Loading.hide()
      Swal.fire({
        customClass: { container: 'my-swal' },
        position: 'center',
        icon: 'success',
        title: 'Proceso exitoso',
        showConfirmButton: false,
        timer: 1500
      })
    }
    return response
  }, async (error) => {
    Loading.hide()

    // session expired
    if (error.response.status >= 401) {
      const store = useAuthStore()

      store.logout()

      router.push({
        name: 'login',
        query: { redirect: urlPath }
      })
      return Promise.reject(error)
    }

    if (error.response.data instanceof Blob) {
      await error.response.data.text().then(response => {
        dispararError('ADVERTENCIA', response)
      })
      return Promise.reject(error)
    }
    // Internal Server Error
    if (error.response.status >= 500) {
      dispararError(`ERROR ${error.response.status}`, error.response.data.detail)
      return Promise.reject(error)
    }

    // error with message
    if (error.response?.data?.detail) {
      dispararError('ADVERTENCIA', error.response.data.detail)
      return Promise.reject(error)
    }

    // error 404
    if (error.response.status === 404) {
      dispararError('ADVERTENCIA', 'No se encontró el recurso')
      return Promise.reject(error)
    }

    const errors = Object.entries(error.response.data)

    let message = ''
    for (const item of errors) {
      message += `${item[0]}: ${item[1]} <br>`
    }

    dispararError('ADVERTENCIA', message)
    return Promise.reject(error)
  })

  app.config.globalProperties.$axios = axios
  app.config.globalProperties.$api = api
})

export { api }
