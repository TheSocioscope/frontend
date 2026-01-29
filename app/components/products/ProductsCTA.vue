<template>
  <section class="section cta-section">
    <div class="container">
      <div class="cta-content">
        <h2>{{ $t('products.cta.title') }}</h2>
        <p>{{ $t('products.cta.description') }}</p>
        <div class="btn-group">
          <v-btn :to="localePath('/products')" class="btn-primary" size="large" elevation="0">
            {{ $t('products.cta.submitButton') }}
          </v-btn>
          <v-btn
            :to="localePath('/about')"
            class="btn-outline"
            size="large"
            variant="outlined"
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
  text-align: center;
  border-top: 3px solid $green-bright;
  padding: 5rem 0;

  @media (max-width: 768px) {
    padding: 4rem 0;
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.cta-content {
  max-width: 700px;
  margin: 0 auto;

  h2 {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    color: $brown-dark;

    @media (max-width: 768px) {
      font-size: 2rem;
    }
  }

  p {
    font-size: 1.2rem;
    margin-bottom: 2.5rem;
    line-height: 1.7;
    font-family: $font-family-display;
    color: $brown-dark;
  }
}

.btn-group {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    flex-direction: column;
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
