<template>
  <h2 class="section-title">
    <v-icon class="section-icon" size="small">{{ icon }}</v-icon>
    <span><slot /></span>
  </h2>
</template>

<script setup lang="ts">
defineProps<{
  icon: string
}>()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section-title {
  display: flex;
  align-items: center;
  gap: $rhythm-1;
  font-size: 1.5rem;
  font-weight: 700;
  color: $green-dark;
  line-height: 1.2;
  margin: 0 0 $rhythm-3;

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 1.125rem;
    margin-bottom: $rhythm-2;
  }
}

.section-icon {
  color: $green-bright;
  flex-shrink: 0;
}
</style>
