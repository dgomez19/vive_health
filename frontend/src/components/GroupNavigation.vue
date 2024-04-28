<template>

  <can :I="action" :an="module">
    <q-expansion-item
      dense-toggle
      :icon="icon"
      :label="title"
      class="q-ma-sm navigation-item"
    >
      <item-navigation v-for="(item, i) in subitems" :key="i + 1" v-bind="item"/>
    </q-expansion-item>
  </can>

</template>

<script setup>
import ItemNavigation from './ItemNavigation.vue'

defineProps({
  icon: String,
  title: String,
  subitems: Array,
  action: String,
  module: String
})
</script>

<style lang="scss">
.navigation-item {
  border-radius: 5px;
}

.tab-active {
  background-color: $primary;
}
</style>
