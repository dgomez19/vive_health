import { defineStore } from 'pinia'
import { api } from 'boot/axios'
import { definePermissions } from 'src/utils/casl'
import { ability } from 'boot/casl'

export const useAuthStore = defineStore('users', {
  state: () => ({
    uuid: '',
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    role: { code: '', text: '' },
    token: '',
    exp: 0
  }),

  getters: {
    expiredToken: () => {
      const currentDate = new Date()
      const _date = this.exp ? new Date(this.exp) : currentDate

      return _date <= currentDate
    },

    fullName: () => `${this.first_name?.trim() || ''} ${this.last_name?.trim() || ''}`
  },

  actions: {
    async login (arg) {
      try {
        const { data } = await api.post('security/login/', arg)

        this.token = data.token
        this.exp = data.exp

        // assign all user variables to `state`
        Object.assign(this, data.user)

        const rules = definePermissions({ role: this.role })

        // update permissions
        ability.update(rules)

        return data
      } catch (err) {}
    },

    async switchSession (arg) {
      try {
        const { data } = await api.post(`security/users/${arg.uuid}/login/`)

        this.token = data.token
        this.exp = data.exp

        // assign all user variables to `state`
        Object.assign(this, data.user)

        const rules = definePermissions({ role: this.role })

        // update permissions
        ability.update(rules)
      } catch (err) {}
    },

    update (data) {
      Object.assign(this, data)
    },

    userLoggedin () {
      return !!this.token
    },

    logout () {
      const rules = definePermissions({})

      ability.update(rules)

      this.$reset()
    }
  },
  persist: { enabled: true }
})
