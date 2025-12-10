<template>
  <div>
    <!-- Hero Section with Video -->
    <HeroBanner />

    <!-- Vision Section -->
    <VisionSection />

    <!-- World Map -->
    <WorldMapSection />

    <!-- Statistics Counter -->
    <StatsSection />

    <!-- Stories from the Field -->
    <StoriesSection />

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
