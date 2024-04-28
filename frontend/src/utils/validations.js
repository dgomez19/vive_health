export const password = val => {
  if (!/[A-ZÑÁÉÍÓÚÜ]+/.test(val)) return 'Mínimo una mayúscula.'

  if (!/[a-zñáéíóú]+/.test(val)) return 'Mínimo una minúscula.'

  if (!/[!"#$%&'()*+,\-./:;<=>?@[\\\]^_¿`{|}~]+/.test(val)) return 'Mínimo un símbolo (!"#$%&\'()*+,-./:;<=>?@[]^_¿`{|}~\\).'

  if (!/[0-9]+/.test(val)) return 'Mínimo un numero.'

  if (val.length < 6 || val.length > 16) return 'Mínimo 6 caracteres y máximo 16 caracteres.'

  return true
}

import moment from 'moment'

export const validarFecha = (formato = 'YYYY/MM/DD') => {
  return val => (!val?.length || moment(val, formato, true).isValid()) || `La fecha ingresada no cumple con el formato "${formato}".`
}

export const obligatorio = val => (val !== null && val !== undefined && val !== '') || 'Este campo es obligatorio'
