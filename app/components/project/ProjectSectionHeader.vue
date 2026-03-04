<template>
  <v-card-title class="section-title">
    <v-icon class="mr-2">{{ icon }}</v-icon>
    <slot />
  </v-card-title>
</template>

<script setup lang="ts">
defineProps<{
  icon: string
}>()
</script>

<style scoped lang="scss">
.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
}
</style>
