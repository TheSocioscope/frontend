<template>
  <section class="cta">
    <div class="container section-header">
      <h2>{{ $t('cta.title') }}</h2>
      <p class="cta-description">{{ $t('cta.description') }}</p>
      <NuxtLink :to="localePath('/projects')" class="btn">{{ $t('cta.button') }}</NuxtLink>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const localePath = useLocalePath()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.cta {
  padding: 6rem 0;
  background: $warm-beige;
  text-align: center;
}

.cta-description {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 2rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
  color: $brown-dark;
}

.btn {
  display: inline-block;
  padding: 1rem 2.5rem;
  background: $green-bright;
  color: white;
  text-decoration: none;
  font-weight: $font-weight-semibold;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  cursor: pointer;

  &:hover {
    background: $forest-green;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(76, 160, 73, 0.3);
  }
}
</style>
