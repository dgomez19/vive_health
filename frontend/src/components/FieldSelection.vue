<template>
  <q-select
    :value="value"
    :options="filteredOptions"
    :option-value="optionValue"
    :option-label="optionLabel"
    @filter="filterFn"
    v-bind="attrs" />
</template>

<script setup>
import { ref, onMounted, useAttrs } from 'vue'
import { api } from 'boot/axios'

onMounted(() => {
  loadOptions()
})

const props = defineProps({
  value: { default: null },
  options: Array,
  optionValue: { type: String, default: 'code' },
  optionLabel: { type: String, default: 'text' },
  url: { type: String, default: null }
})

const attrs = useAttrs()

const filteredOptions = ref([])
let localOptions = []

const removeAccents = str => str.normalize('NFD').replace(/[\u0300-\u036f]/g, '')

const includes = (option, val) => {
  const cleanOption = removeAccents(option[props.optionLabel]).toLowerCase()
  const cleanValue = removeAccents(val).toLowerCase()

  return cleanOption.includes(cleanValue)
}

const loadOptions = async () => {
  if (props.options) {
    localOptions = [...props.options]
    return
  }

  if (!props.url) return

  try {
    const { data } = await api.get(props.url)

    localOptions = [...data]
  } catch (err) {
    localOptions = []
  }
}

const filterFn = (val, update) => {
  if (val === '') {
    filteredOptions.value = [...localOptions]
  } else {
    filteredOptions.value = localOptions.filter(option => includes(option, val))
  }
  update()
}
</script>
