<template>
  <div>
    <!-- Hero Section with Video -->
    <HeroBanner />

    <!-- Microscope Section -->
    <MicroscopeSection />

    <!-- Vision Section -->
    <VisionSection />

    <!-- Scientific Breakthroughs -->
    <BreakthroughSection />

    <!-- Statistics Counter -->
    <StatsSection />

    <!-- Stories from the Field -->
    <StoriesSection />

    <!-- World Map -->
    <WorldMapSection />

    <!-- Newsletter -->
    <NewsletterSection />

    <!-- Partners -->
    <PartnersSection />
  </div>
</template>

<script setup lang="ts">
const { t, locale } = useI18n()

// SEO
useHead({
  title: t('hero.title'),
  meta: [
    {
      name: 'description',
      content: t('hero.tagline')
    },
    {
      property: 'og:title',
      content: t('hero.title')
    },
    {
      property: 'og:description',
      content: t('hero.tagline')
    },
    {
      property: 'og:type',
      content: 'website'
    }
  ]
})
</script>
