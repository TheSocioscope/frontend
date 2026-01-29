<template>
  <section class="section values-section">
    <v-container>
      <div class="section-header">
        <h2>{{ $t('about.values.title') }}</h2>
      </div>
      <div class="values-grid">
        <div v-for="(value, index) in values" :key="index" class="value-card">
          <div class="value-icon">{{ value.icon }}</div>
          <h3>{{ $t(value.titleKey) }}</h3>
          <p>{{ $t(value.descKey) }}</p>
        </div>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const values = [
  {
    icon: '🌍',
    titleKey: 'about.values.global.title',
    descKey: 'about.values.global.desc'
  },
  {
    icon: '🤝',
    titleKey: 'about.values.collaboration.title',
    descKey: 'about.values.collaboration.desc'
  },
  {
    icon: '🔓',
    titleKey: 'about.values.open.title',
    descKey: 'about.values.open.desc'
  },
  {
    icon: '⚖️',
    titleKey: 'about.values.ethical.title',
    descKey: 'about.values.ethical.desc'
  }
]
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.values-section {
  background: $warm-beige;
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
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 3rem;
  max-width: 900px;
  margin: 0 auto;

  @media (max-width: 1024px) {
    grid-template-columns: 1fr;
  }
}

.value-card {
  text-align: center;

  .value-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  h3 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: $forest-green;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
  }

  p {
    line-height: 1.7;
    color: $brown-dark;
    opacity: 0.8;
    font-family: $font-family-display;
  }
}
</style>
