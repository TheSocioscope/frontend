<template>
  <div>
    <!-- Hero Banner -->
    <PageHero
      :title="$t('research.hero.title', 'Food Socioscope Research')"
      :subtitle="$t('research.hero.subtitle', 'What research insights do you need?')"
      icon="mdi-magnify"
      compact
      centered
    />

    <!-- Main Form -->
    <div class="research-container">
      <ResearchForm />
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

definePageMeta({
  layout: 'default',
})

useHead({
  title: t('research.meta.title', 'Food Socioscope Research'),
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.research-container {
  background: $cream;
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1rem;

  @media (max-width: 768px) {
    margin: 1rem auto;
  }
}
</style>
