<template>
  <div>
    <PageHero :title="$t('terms.hero.title')" :subtitle="$t('terms.hero.subtitle')" icon="mdi-file-document-outline" compact />

    <section class="section legal-section">
      <div class="container">
        <div v-if="page" class="legal-content">
          <p class="last-updated">{{ $t('privacy.lastUpdated') }}: {{ formatDate(page.lastUpdated) }}</p>

          <ContentRenderer :value="page" class="prose" />
        </div>
        <div v-else class="legal-content">
          <p class="text-center">{{ $t('common.loading') }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t, t: $t, locale } = useI18n()

useHead({
  title: t('terms.meta.title')
})

const MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']
const formatDate = (val: unknown) => {
  const str = typeof val === 'string' ? val : String(val ?? '')
  const parts = str.slice(0, 10).split('-')
  if (parts.length !== 3) return str
  const [y, m, d] = parts.map(Number)
  return `${MONTHS[m - 1]} ${d}, ${y}`
}

const { data: page } = await useAsyncData(
  `terms-${locale.value}`,
  async () => {
    const localized = await queryCollection('pages')
      .where('path', 'LIKE', `/pages/${locale.value}/terms%`)
      .first()

    if (localized) return localized

    return (
      (await queryCollection('pages')
        .where('path', 'LIKE', '/pages/en/terms%')
        .first()) || null
    )
  },
  { watch: [locale] }
)
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.legal-section {
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

.legal-content {
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

  :deep(ul) {
    margin-left: 2rem;
    margin-bottom: 1rem;

    li {
      margin-bottom: 0.75rem;
      line-height: 1.7;
      font-family: $font-family-display;
      color: $brown-dark;
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
