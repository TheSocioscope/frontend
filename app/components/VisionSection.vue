<template>
  <section class="section vision-section">
    <v-container>
      <div class="vision-content">
        <h2 class="section-title text-center mb-8">{{ $t('vision.title') }}</h2>
        <p class="vision-statement text-center">
          {{ $t('vision.statement') }}
        </p>
        <p class="vision-details text-center">
          {{ $t('vision.details1') }}
        </p>
        <p class="vision-details text-center" style="margin-top: 30px">
          <strong>{{ $t('vision.details2') }}</strong>
        </p>
      </div>

      <v-row class="contributions-grid mt-12">
        <v-col v-for="i in 3" :key="i" cols="12" md="4">
          <v-card class="contribution-card h-100" elevation="2">
            <v-card-text>
              <div class="contribution-icon">{{ $t(`contributions.card${i}.icon`) }}</div>
              <h3 class="mb-4">{{ $t(`contributions.card${i}.title`) }}</h3>
              <p class="mb-3">{{ $t(`contributions.card${i}.description`) }}</p>
              <p v-if="$t(`contributions.card${i}.description2`)" class="mb-3">
                {{ $t(`contributions.card${i}.description2`) }}
              </p>
              <a v-if="$t(`contributions.card${i}.link`)" href="#" class="contribution-link">
                {{ $t(`contributions.card${i}.link`) }}
              </a>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.vision-section {
  background: $surface-cream;
}

.vision-content {
  max-width: 900px;
  margin: 0 auto;
  text-align: center;

  h2 {
    font-size: 3rem;
    color: $brown-medium;
    margin-bottom: $spacing-xl;
    font-weight: 400;

    @media (max-width: 768px) {
      font-size: 2rem;
    }
  }
}

.vision-statement {
  font-size: 1.5rem;
  color: $brown-dark;
  margin-bottom: $spacing-lg;
  line-height: 1.7;
  font-weight: 300;

  @media (max-width: 768px) {
    font-size: 1.2rem;
  }
}

.vision-details {
  font-size: 1.2rem;
  color: $brown-dark;
  line-height: 1.8;
  margin-bottom: $spacing-md;

  @media (max-width: 768px) {
    font-size: 1rem;
  }
}

.contributions-grid {
  margin-top: $spacing-4xl;
}

.contribution-card {
  background: $surface-cream !important;
  padding: $spacing-lg;
  border: 2px solid $cream-dark !important;
  transition:
    transform 0.3s,
    box-shadow 0.3s;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1) !important;
  }
}

.contribution-icon {
  font-size: 3rem;
  margin-bottom: $spacing-md;
  display: block;
}

.contribution-card h3 {
  font-size: 1.8rem;
  color: $brown-dark;
  margin-bottom: $spacing-md;
  font-weight: 500;
}

.contribution-card p {
  font-size: 1.1rem;
  color: $brown-medium;
  line-height: 1.7;
  margin-bottom: $spacing-md;
}

.contribution-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: #2e7d32;
  text-decoration: none;
  font-weight: 500;
  margin-top: 10px;
  transition: gap 0.3s;

  &:hover {
    gap: 12px;
  }
}
</style>
