<template>
  <section :class="['section', { 'section-beige': beige }]">
    <div class="container">
      <h2 class="section-title">{{ title }}</h2>
      <p v-if="description" class="section-description">{{ description }}</p>
      <slot name="search" />
      <div class="team-grid">
        <slot />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description?: string
  beige?: boolean
}>()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section {
  padding: 3rem 0;
}

.section-beige {
  background: $warm-beige;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.section-title {
  text-align: center;
  font-family: 'Playfair Display', serif;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.section-description {
  text-align: center;
  font-size: 1.1rem;
  opacity: 0.7;
  max-width: 600px;
  margin: 0 auto 3rem;
}

.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 2rem;
}
</style>
