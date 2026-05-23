<template>
  <section class="section cta-section">
    <div class="container">
      <div class="cta-row section-reveal">
        <div class="cta-text">
          <h2>{{ $t('products.cta.title') }}</h2>
          <p>{{ $t('products.cta.description') }}</p>
        </div>
        <div class="btn-group">
          <v-btn
            :to="localePath('/about')"
            class="btn-primary"
            size="large"
            elevation="0"
          >
            {{ $t('products.cta.learnMoreButton') }}
          </v-btn>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const localePath = useLocalePath()
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.cta-section {
  background: $warm-beige;
  border-top: 3px solid $green-bright;
  padding: 2.5rem 0;

  @media (max-width: 768px) {
    padding: 2rem 0;
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;

  @media (max-width: 768px) {
    padding: 0 1rem;
  }
}

.cta-row {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 2rem;
  align-items: center;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
}

.cta-text {
  h2 {
    font-size: 1.875rem;
    margin: 0 0 0.5rem;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    color: $brown-dark;
    line-height: 1.2;

    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
  }

  p {
    font-size: 1rem;
    line-height: 1.55;
    font-family: $font-family-display;
    color: $brown-dark;
    opacity: 0.85;
    margin: 0;
  }
}

.btn-group {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: flex-end;

  @media (max-width: 768px) {
    justify-content: stretch;
  }
}

.btn-primary {
  background: $green-bright !important;
  color: white !important;
  border: 2px solid $green-bright !important;
  font-weight: $font-weight-semibold !important;
  font-family: $font-family-display !important;
  transition: all 0.3s ease !important;
  padding: 1rem 2.5rem !important;
  height: auto !important;
  min-height: auto !important;
  display: inline-flex !important;
  align-items: center !important;

  &:hover {
    background: $forest-green !important;
    border-color: $forest-green !important;
  }

  @media (max-width: 768px) {
    width: 100%;
  }
}

.btn-outline {
  background: transparent !important;
  color: $brown-dark !important;
  border: 2px solid $brown-dark !important;
  font-weight: $font-weight-semibold !important;
  font-family: $font-family-display !important;
  transition: all 0.3s ease !important;
  padding: 1rem 2.5rem !important;
  height: auto !important;
  min-height: auto !important;
  display: inline-flex !important;
  align-items: center !important;

  &:hover {
    background: $brown-dark !important;
    color: $cream !important;
  }

  @media (max-width: 768px) {
    width: 100%;
  }
}
</style>
