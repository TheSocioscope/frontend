<template>
  <section class="section what-we-do-section">
    <v-container>
      <div class="section-header">
        <h2>{{ $t('about.whatWeDo.title') }}</h2>
      </div>
      <div class="content-wrapper">
        <div class="content-text">
          <p>{{ $t('about.whatWeDo.paragraph1') }}</p>
          <p>{{ $t('about.whatWeDo.paragraph2') }}</p>
        </div>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.what-we-do-section {
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
</style>
