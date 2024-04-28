import { Can, abilitiesPlugin } from '@casl/vue'
import { defineAbility } from '@casl/ability'
import { definePermissions } from 'src/utils/casl'
import { useAuthStore } from 'src/stores/auth'

export const ability = defineAbility(() => {})

export default async ({ app }) => {
  const store = useAuthStore()

  const rules = definePermissions({ role: store?.role })

  ability.update(rules)

  app.use(abilitiesPlugin, ability, { useGlobalProperties: true })
  app.component('Can', Can) // eslint-disable-line
}
