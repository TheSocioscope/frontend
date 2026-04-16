<template>
  <section class="section vision-section">
    <v-container>
      <div class="section-header">
        <h2>
          {{ $t('vision.title') }}
        </h2>
        <p class="vision-statement">
          {{ $t('vision.statement1') }}
        </p>
        <p v-if="$t('vision.statement2')" class="vision-statement mt-4">
          {{ $t('vision.statement2') }}
        </p>
      </div>

      <v-row class="contributions-grid mt-12">
        <v-col v-for="(icon, i) in contributionIcons" :key="i" cols="12" md="4">
          <v-card class="contribution-card h-100" elevation="2">
            <v-card-text>
              <div class="contribution-icon" aria-hidden="true">
                <v-icon size="2.5rem">{{ icon }}</v-icon>
              </div>
              <h3 class="text-h5 font-weight-medium mb-4">
                {{ $t(`contributions.card${i + 1}.title`) }}
              </h3>
              <p class="text-body-2 mb-3">{{ $t(`contributions.card${i + 1}.description`) }}</p>
              <p v-if="$t(`contributions.card${i + 1}.description2`)" class="text-body-2 mb-3">
                {{ $t(`contributions.card${i + 1}.description2`) }}
              </p>
              <a
                v-if="$t(`contributions.card${i + 1}.link`)"
                href="#"
                class="contribution-link text-body-2 font-weight-medium"
              >
                {{ $t(`contributions.card${i + 1}.link`) }}
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

const contributionIcons = ['mdi-database-outline', 'mdi-chip', 'mdi-chart-line']
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.vision-section {
  background: $surface-cream;
}

.vision-statement {
  font-size: 1.1rem;
  line-height: 1.8;
  color: $brown-dark;
}

.contributions-grid {
  margin-top: $spacing-4xl;
}

.contribution-card {
  background: white;
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
  margin-bottom: $spacing-md;
  display: block;
  color: $green-bright;
}

.contribution-card h3 {
  color: $green-bright;
  font-family: $font-family-display;
}

.contribution-card p {
  color: $brown-medium;
  line-height: 1.6;
}

.contribution-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  color: $green-medium;
  text-decoration: none;
  font-weight: $font-weight-medium;
  margin-top: 10px;
  transition: gap 0.3s;

  &:hover {
    gap: 12px;
  }
}
</style>
