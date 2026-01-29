<template>
  <section class="section mission-section">
    <v-container>
      <div class="section-header">
        <h2>{{ $t('about.mission.title') }}</h2>
      </div>
      <div class="content-wrapper">
        <div class="content-text">
          <p>{{ $t('about.mission.paragraph1') }}</p>
          <p>{{ $t('about.mission.paragraph2') }}</p>
        </div>
        <div class="info-grid">
          <div v-for="(item, index) in infoItems" :key="index" class="info-item">
            <span class="info-icon">{{ item.icon }}</span>
            <h3>{{ $t(item.labelKey) }}</h3>
            <p>{{ $t(item.valueKey) }}</p>
            <div class="info-detail">{{ $t(item.detailKey) }}</div>
          </div>
        </div>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const infoItems = [
  {
    icon: '🌱',
    labelKey: 'about.info.established.label',
    valueKey: 'about.info.established.value',
    detailKey: 'about.info.established.detail'
  },
  {
    icon: '🥐',
    labelKey: 'about.info.location.label',
    valueKey: 'about.info.location.value',
    detailKey: 'about.info.location.detail'
  },
  {
    icon: '🌍',
    labelKey: 'about.info.reach.label',
    valueKey: 'about.info.reach.value',
    detailKey: 'about.info.reach.detail'
  }
]
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.mission-section {
  background: $cream;
  padding: 5rem 0;
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

.content-wrapper {
  max-width: 800px;
  margin: 0 auto;
}

.content-text {
  p {
    margin-bottom: 1.5rem;
    font-size: 1.1rem;
    line-height: 1.8;
    font-family: $font-family-display;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 3rem;
  margin-top: 4rem;
  padding: 3rem 0 0;
  border-top: 3px solid $green-bright;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}

.info-item {
  text-align: center;
  position: relative;
  padding: 2rem 1.5rem;
  background: $cream;
  border: 2px solid $warm-beige;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    border-color: $green-bright;
    box-shadow: 0 8px 20px rgba(76, 160, 73, 0.15);
  }

  .info-icon {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    display: block;
  }

  h3 {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: $forest-green;
    margin-bottom: 0.75rem;
    font-weight: $font-weight-semibold;
    font-family: $font-family-display;
  }

  p {
    font-size: 1.3rem;
    font-weight: $font-weight-bold;
    color: $brown-dark;
    line-height: 1.4;
    font-family: $font-family-display;
  }

  .info-detail {
    font-size: 0.95rem;
    font-weight: $font-weight-regular;
    color: $brown-dark;
    opacity: 0.7;
    margin-top: 0.5rem;
    font-family: $font-family-display;
  }
}
</style>
