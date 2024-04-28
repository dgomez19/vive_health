import { boot } from 'quasar/wrappers'
import VueSweetalert2 from 'vue-sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'

export default boot(({ app }) => {
  app.use(VueSweetalert2)
})
