<template>
  <section class="section cta-section">
    <v-container>
      <div class="cta-content">
        <h2>{{ $t('about.cta.title') }}</h2>
        <p>{{ $t('about.cta.description') }}</p>
        <div class="btn-group">
          <v-btn :to="localePath('/projects')" class="btn-primary" size="large" elevation="0">
            {{ $t('about.cta.submitButton') }}
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
  padding: 5rem 0;

  @media (max-width: 768px) {
    padding: 4rem 0;
  }
}

.cta-content {
  text-align: center;
  max-width: 700px;
  margin: 0 auto;

  h2 {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    color: $brown-dark;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;

    @media (max-width: 768px) {
      font-size: 2rem;
    }
  }

  p {
    font-size: 1.2rem;
    margin-bottom: 2.5rem;
    color: $brown-dark;
    line-height: 1.7;
    font-family: $font-family-display;
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
