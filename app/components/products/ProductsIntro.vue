<template>
  <div class="intro-section">
    <h2>{{ $t('products.intro.title') }}</h2>
    <p>{{ $t('products.intro.description') }}</p>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.intro-section {
  max-width: 760px;
  margin: 0 auto 1.75rem;
  text-align: center;

  h2 {
    font-size: 2rem;
    margin: 0 0 0.75rem;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    color: $brown-dark;
    line-height: 1.15;

    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
  }

  p {
    font-size: 1rem;
    line-height: 1.65;
    opacity: 0.8;
    font-family: $font-family-display;
    color: $brown-dark;
    margin: 0;

    @media (max-width: 768px) {
      font-size: 0.9375rem;
    }
  }
}
</style>
