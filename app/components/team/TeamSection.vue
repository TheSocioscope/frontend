<template>
  <section :class="['section', { 'section-beige': beige }]">
    <div class="container">
      <div class="section-reveal">
        <h2 class="section-title">{{ title }}</h2>
        <p v-if="description" class="section-description">{{ description }}</p>
      </div>
      <slot name="search" />
      <div class="team-grid section-reveal">
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

  @media (max-width: 600px) {
    padding: 1.75rem 0;
  }
}

.section-beige {
  background: $warm-beige;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;

  @media (max-width: 600px) {
    padding: 0 1rem;
  }
}

.section-title {
  text-align: center;
  font-family: $font-family-base;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
  font-weight: 700;

  @media (max-width: 600px) {
    text-align: left;
    font-size: 1.5rem;
    margin-bottom: 0.25rem;
  }
}

.section-description {
  text-align: center;
  font-size: 1.1rem;
  opacity: 0.7;
  max-width: 600px;
  margin: 0 auto 3rem;

  @media (max-width: 600px) {
    text-align: left;
    font-size: 0.875rem;
    margin: 0 0 1.25rem;
    line-height: 1.45;
  }
}

/* Cards are fixed-width tracks (280px) and the grid centers the group.
   This keeps small sections like "Principal Investigators" centered
   instead of left-aligned with empty space, while larger sections still
   fill rows naturally. */
.team-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, 280px);
  justify-content: center;
  gap: 2rem;

  @media (max-width: 600px) {
    /* Mobile keeps the dense 2-col fill — center justification would
       leave awkward gutters at this size. */
    grid-template-columns: repeat(2, 1fr);
    justify-content: stretch;
    gap: 1rem 0.75rem;
  }
}
</style>
