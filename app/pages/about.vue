<template>
  <div>
    <PageHero :title="$t('about.hero.title')" :subtitle="$t('about.hero.subtitle')" icon="🌿" />
    <AboutMission />
    <AboutWhatWeDo />
    <AboutMethodology />
    <AboutValues />
    <AboutCTA />
  </div>
</template>

<script setup lang="ts">
const { t, t: $t } = useI18n()

useHead({
  title: t('about.meta.title')
})
</script>
