<template>
  <div>
    <!-- Hero Banner -->
    <PageHero
      :title="$t('research.hero.title', 'Food Socioscope Research Project')"
      :subtitle="$t('research.hero.subtitle', 'What research insights are you interested in')"
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

const pageTitle = t('research.meta.title', 'Food Socioscope Research Project')
const pageDescription = t('research.meta.description', 'Access free strategic research outputs including SWOT analysis, benchmarking reports, and peer learning sessions. Discover what research insights would be most valuable for your initiative.')

useHead({
  title: pageTitle,
  meta: [
    {
      name: 'description',
      content: pageDescription
    },
    {
      name: 'keywords',
      content: 'research, SWOT analysis, benchmarking, food systems, strategic insights, peer learning, sustainability'
    },
    {
      property: 'og:title',
      content: pageTitle
    },
    {
      property: 'og:description',
      content: pageDescription
    },
    {
      property: 'og:type',
      content: 'website'
    },
    {
      property: 'og:url',
      content: 'https://thesocioscope.org/research'
    },
    {
      property: 'og:image',
      content: 'https://thesocioscope.org/og-image.png'
    },
    {
      name: 'twitter:card',
      content: 'summary_large_image'
    },
    {
      name: 'twitter:title',
      content: pageTitle
    },
    {
      name: 'twitter:description',
      content: pageDescription
    },
    {
      name: 'twitter:image',
      content: 'https://thesocioscope.org/og-image.png'
    }
  ],
  link: [
    {
      rel: 'canonical',
      href: 'https://thesocioscope.org/research'
    }
  ]
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
