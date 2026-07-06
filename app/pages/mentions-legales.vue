<template>
  <div>
    <PageHero :title="$t('mentionsLegales.hero.title')" :subtitle="$t('mentionsLegales.hero.subtitle')" icon="mdi-gavel" compact />

    <section class="section legal-section">
      <div class="container">
        <div v-if="page" class="legal-content">
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
  title: t('mentionsLegales.meta.title')
})

const { data: page } = await useAsyncData(
  'mentions-legales',
  async () => {
    return (
      (await queryCollection('pages')
        .where('path', 'LIKE', '/pages/en/mentions-legales%')
        .first()) || null
    )
  }
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
