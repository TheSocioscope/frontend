<template>
  <section class="section microscope-section">
    <v-container>
      <v-row align="center">
        <!-- Visual -->
        <v-col cols="12" md="6" class="text-center">
          <div class="microscope-visual">
            {{ $t('microscope.icon') }}
          </div>
        </v-col>

        <!-- Content -->
        <v-col cols="12" md="6">
          <div class="microscope-content">
            <h2 class="text-h3 text-md-h2 font-weight-medium mb-6">{{ $t('microscope.title') }}</h2>
            <p class="text-body-1 mb-4">
              {{ $t('microscope.description1') }}
            </p>
            <p class="text-body-1">
              {{ $t('microscope.description2') }}
            </p>
          </div>
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

.microscope-section {
  background: white;
}

.microscope-visual {
  font-size: 10rem;
  color: $green-medium;
  opacity: 0.2;

  @media (max-width: 768px) {
    font-size: 6rem;
  }
}

.microscope-content {
  h2 {
    color: $brown-medium;
  }

  p {
    color: $brown-dark;
    line-height: 1.7;
  }
}
</style>
