<template>
  <can :I="action" :an="module">
    <q-item exact clickable v-ripple :to="route" class="q-ma-sm navigation-item" active-class="tab-active">
      <q-item-section avatar>
        <q-icon v-if="icon" :name="icon" />
        <q-avatar v-else-if="image" color="primary" text-color="white">
          <q-img :src="image"/>
        </q-avatar>

      </q-item-section>

      <q-item-section>
        <q-item-label>{{ title }}</q-item-label>
        <q-item-label caption class="text-grey-5">{{ subtitle }}</q-item-label>
      </q-item-section>

      <q-item-section v-if="sideIcon" side>
        <q-icon :name="sideIcon"/>
      </q-item-section>

    </q-item>
  </can>
</template>

<script setup>
defineProps({
  route: String,
  icon: { type: String, default: null },
  image: { type: String, default: null },
  sideIcon: { type: String, default: null },
  title: String,
  subtitle: String,
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
