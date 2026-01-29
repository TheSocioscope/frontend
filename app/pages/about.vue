<template>
  <div>
    <AboutHero />
    <AboutMission />
    <AboutWhatWeDo />
    <AboutMethodology />
    <AboutValues />
    <AboutCTA />
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: t('about.meta.title')
})
</script>
