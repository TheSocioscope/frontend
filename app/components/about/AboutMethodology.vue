<template>
  <section class="section methodology-section">
    <v-container>
      <div class="section-header">
        <h2>{{ $t('about.methodology.title') }}</h2>
        <p class="subtitle">{{ $t('about.methodology.subtitle') }}</p>
      </div>
      <div class="method-grid">
        <div v-for="(method, index) in methods" :key="index" class="method-card">
          <div class="method-number">{{ String(index + 1).padStart(2, '0') }}</div>
          <h3>{{ $t(method.titleKey) }}</h3>
          <p>{{ $t(method.descKey) }}</p>
        </div>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const methods = [
  {
    titleKey: 'about.methodology.step1.title',
    descKey: 'about.methodology.step1.desc'
  },
  {
    titleKey: 'about.methodology.step2.title',
    descKey: 'about.methodology.step2.desc'
  },
  {
    titleKey: 'about.methodology.step3.title',
    descKey: 'about.methodology.step3.desc'
  },
  {
    titleKey: 'about.methodology.step4.title',
    descKey: 'about.methodology.step4.desc'
  }
]
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.methodology-section {
  background: $cream;
  padding: 5rem 0;

  @media (max-width: 768px) {
    padding: 4rem 0;
  }
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;

  h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: $brown-dark;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;

    @media (max-width: 768px) {
      font-size: 2rem;
    }
  }

  .subtitle {
    font-size: 1.1rem;
    color: $brown-dark;
    opacity: 0.7;
    font-family: $font-family-display;
  }
}

.method-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.method-card {
  background: $cream;
  padding: 2rem;
  border: 2px solid $warm-beige;
  text-align: center;

  .method-number {
    font-size: 2.5rem;
    font-weight: $font-weight-bold;
    color: $green-bright;
    margin-bottom: 1rem;
    line-height: 1;
    font-family: $font-family-display;
  }

  h3 {
    font-size: 1.4rem;
    margin-bottom: 1rem;
    color: $brown-dark;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
  }

  p {
    font-size: 1rem;
    line-height: 1.7;
    color: $brown-dark;
    opacity: 0.8;
    font-family: $font-family-display;
  }
}
</style>
