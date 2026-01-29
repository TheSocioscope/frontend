<template>
  <section class="submit-cta-section">
    <div class="container">
      <h2>{{ $t('resources.cta.title') }}</h2>
      <p>{{ $t('resources.cta.subtitle') }}</p>
      <button class="btn" @click="$emit('submit')">
        {{ $t('resources.cta.button') }}
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
defineEmits<{
  submit: []
}>()
</script>

<style scoped lang="scss">
@use 'sass:color';
@use '../../../assets/styles/variables' as *;

.submit-cta-section {
  background: linear-gradient(
    135deg,
    $green-bright 0%,
    color.adjust($green-bright, $lightness: -10%) 100%
  );
  color: white;
  text-align: center;
  padding: 5rem 2rem;

  @media (max-width: 768px) {
    padding: 4rem 1.5rem;
  }

  h2 {
    font-family: $font-family-display;
    font-size: 2.5rem;
    margin-bottom: 1rem;

    @media (max-width: 768px) {
      font-size: 2rem;
    }
  }

  p {
    font-size: 1.25rem;
    opacity: 0.95;
    margin-bottom: 2rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
  }

  .btn {
    background: white;
    color: $green-bright;
    padding: 1rem 2.5rem;
    font-size: 1.1rem;
    font-weight: 600;
    border-radius: 0;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    display: inline-flex;
    align-items: center;
    height: auto;
    min-height: auto;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
    }
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
}
</style>
