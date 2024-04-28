import { QBadge, QBtn } from 'quasar'
import { h } from 'vue'

export const badge = (choice, colors) => h(QBadge, {
  color: colors[choice.code],
  label: choice.text
})

export const tableBtn = ({ color = 'primary', size = '10px', ...args }) => h(QBtn, {
  unelevated: true,
  round: true,
  color,
  size,
  ...args
})
