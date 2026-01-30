<template>
  <div>
    <PageHero :title="$t('privacy.hero.title')" :subtitle="$t('privacy.hero.subtitle')" icon="🔒" />

    <section class="section privacy-section">
      <div class="container">
        <div v-if="page" class="privacy-content">
          <p class="last-updated">
            {{ $t('privacy.lastUpdated') }}:
            {{ new Date(page.lastUpdated).toLocaleDateString(locale) }}
          </p>

          <ContentRenderer :value="page" class="prose" />
        </div>
        <div v-else class="privacy-content">
          <p class="text-center">{{ $t('common.loading') }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t, t: $t, locale } = useI18n()
const localePath = useLocalePath()

useHead({
  title: t('privacy.meta.title')
})

// Fetch the privacy policy content based on current locale
const { data: page } = await useAsyncData(`privacy-${locale.value}`, async () => {
  const allPages = await queryCollection('pages').all()

  // Find the privacy policy for the current locale
  const localizedPage = allPages.find((item: any) => {
    const isPrivacyPolicy =
      item.slug === 'privacy-policy' ||
      item._path?.includes('privacy-policy') ||
      item.stem?.includes('privacy-policy')
    const isCurrentLocale =
      item._path?.includes(`/${locale.value}/`) || item.stem?.includes(`${locale.value}/`)
    return isPrivacyPolicy && isCurrentLocale
  })

  if (localizedPage) return localizedPage

  // Fallback to English if no localized version found
  return (
    allPages.find((item: any) => {
      const isPrivacyPolicy =
        item.slug === 'privacy-policy' || item._path?.includes('privacy-policy')
      const isEnglish = item._path?.includes('/en/') || item.stem?.includes('en/')
      return isPrivacyPolicy && isEnglish
    }) || null
  )
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.privacy-section {
  background: $cream;
  padding: 5rem 0;

  @media (max-width: 768px) {
    padding: 3rem 0;
  }
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
}

.privacy-content {
  background: white;
  padding: 3rem;
  border: 2px solid $warm-beige;

  @media (max-width: 768px) {
    padding: 2rem 1.5rem;
  }
}

.last-updated {
  font-size: 0.9rem;
  color: $brown-dark;
  opacity: 0.7;
  margin-bottom: 2rem;
  font-style: italic;
  font-family: $font-family-display;
}

.text-center {
  text-align: center;
}

.prose {
  font-family: $font-family-display;
  color: $brown-dark;

  :deep(p) {
    font-size: 1rem;
    line-height: 1.8;
    margin-bottom: 1rem;
  }

  :deep(h2) {
    font-size: 1.8rem;
    color: $brown-dark;
    margin-top: 3rem;
    margin-bottom: 1.5rem;
    font-weight: $font-weight-bold;
    font-family: $font-family-display;
    border-bottom: 2px solid $green-bright;
    padding-bottom: 0.5rem;

    &:first-of-type {
      margin-top: 0;
    }

    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
  }

  :deep(h3) {
    font-size: 1.4rem;
    color: $brown-dark;
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-weight: $font-weight-semibold;
    font-family: $font-family-display;
  }

  :deep(ul) {
    margin-left: 2rem;
    margin-bottom: 1rem;

    li {
      margin-bottom: 0.75rem;
      line-height: 1.7;
      font-family: $font-family-display;
      color: $brown-dark;

      strong {
        color: $forest-green;
        font-weight: $font-weight-semibold;
      }
    }
  }

  :deep(a) {
    color: $forest-green;
    text-decoration: none;
    font-weight: $font-weight-semibold;
    transition: color 0.3s;

    &:hover {
      color: $green-bright;
      text-decoration: underline;
    }
  }

  :deep(strong) {
    font-weight: $font-weight-semibold;
  }
}
</style>
