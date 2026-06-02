<template>
  <section class="section cta-section">
    <v-container>
      <div class="cta-row section-reveal">
        <div class="cta-text">
          <h2>{{ $t('about.cta.title') }}</h2>
          <p>{{ $t('about.cta.description') }}</p>
        </div>
        <div class="btn-group">
          <v-btn :to="localePath('/projects')" class="btn-primary" size="large" elevation="0">
            {{ $t('nav.projects') }}
          </v-btn>
          <v-btn
            :to="localePath('/contact')"
            class="btn-outline"
            size="large"
            variant="outlined"
            elevation="0"
          >
            {{ $t('about.cta.contactButton') }}
          </v-btn>
        </div>
      </div>
    </v-container>
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
  color: $brown-dark;
  border-top: 3px solid $green-bright;
  padding: 2.5rem 0;

  @media (max-width: 768px) {
    padding: 2rem 0;
  }
}

.cta-row {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.cta-text {
  h2 {
    font-size: 1.875rem;
    margin: 0 0 0.5rem;
    color: $brown-dark;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    line-height: 1.2;

    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
  }

  p {
    font-size: 1rem;
    margin: 0;
    color: $brown-dark;
    line-height: 1.55;
    font-family: $font-family-display;
    opacity: 0.85;
  }
}

.btn-group {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
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
