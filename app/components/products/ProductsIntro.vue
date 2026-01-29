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
  max-width: 800px;
  margin: 0 auto 4rem;
  text-align: center;

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
    font-size: 1.15rem;
    line-height: 1.8;
    opacity: 0.85;
    font-family: $font-family-display;
    color: $brown-dark;
  }
}
</style>
