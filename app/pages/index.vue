<template>
  <div>
    <!-- Hero Section with Animated Circles -->
    <HomepageHeroBanner />

    <!-- Statistics Counter -->
    <HomepageStatsSection />

    <!-- Vision Section -->
    <HomepageVisionSection />

    <!-- World Map -->
    <HomepageWorldMapSection />

    <!-- Stories from the Field -->
    <HomepageStoriesSection />

    <!-- Newsletter -->
    <HomepageNewsletterSection />

    <!-- Call to Join -->
    <HomepageCallToJoinSection />

    <!-- Partners -->
    <HomepagePartnersSection />
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
