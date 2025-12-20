<template>
  <div>
    <!-- Hero -->
    <v-container class="hero-section py-16">
      <v-row align="center">
        <v-col cols="12" md="6">
          <h1 class="text-h2 mb-4">{{ $t('about.title') }}</h1>
          <p class="text-h6">{{ $t('about.subtitle') }}</p>
        </v-col>
        <v-col cols="12" md="6" class="text-center">
          <div style="font-size: 6rem; opacity: 0.3">🌿</div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Mission -->
    <section class="section section-white py-12">
      <v-container>
        <h2 class="text-center mb-8">{{ $t('about.mission.title') }}</h2>
        <v-row justify="center">
          <v-col cols="12" lg="10">
            <p class="text-h6 text-center mb-4">{{ $t('about.mission.text1') }}</p>
            <p class="text-h6 text-center">{{ $t('about.mission.text2') }}</p>
          </v-col>
        </v-row>
        
        <!-- Info Cards -->
        <v-row class="mt-12">
          <v-col v-for="(info, i) in infoCards" :key="i" cols="12" md="4">
            <div class="info-card">
              <span class="info-icon">{{ info.icon }}</span>
              <h3>{{ $t(info.title) }}</h3>
              <div class="info-number">{{ $t(info.value) }}</div>
              <div class="info-detail">{{ $t(info.detail) }}</div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- What We Do -->
    <section class="section section-beige py-12">
      <v-container>
        <h2 class="text-center mb-8">{{ $t('about.whatWeDo.title') }}</h2>
        <v-row justify="center">
          <v-col cols="12" lg="10">
            <p class="text-h6 text-center">{{ $t('about.whatWeDo.text') }}</p>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Methodology -->
    <section class="section section-white py-12">
      <v-container>
        <h2 class="text-center mb-4">{{ $t('about.methodology.title') }}</h2>
        <p class="text-center mb-12">{{ $t('about.methodology.subtitle') }}</p>
        <v-row>
          <v-col v-for="(method, i) in methods" :key="i" cols="12" md="6" lg="3">
            <div class="method-card">
              <div class="method-number">{{ `0${i + 1}` }}</div>
              <h3 class="mb-4">{{ $t(method.title) }}</h3>
              <p>{{ $t(method.description) }}</p>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Values -->
    <section class="section section-beige py-12">
      <v-container>
        <h2 class="text-center mb-12">{{ $t('about.values.title') }}</h2>
        <v-row>
          <v-col v-for="(value, i) in values" :key="i" cols="12" md="6">
            <div class="value-card text-center">
              <div class="value-icon mb-4">{{ value.icon }}</div>
              <h3 class="mb-4">{{ $t(value.title) }}</h3>
              <p>{{ $t(value.description) }}</p>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA -->
    <section class="py-12">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" md="8" class="text-center">
            <h2 class="mb-6">{{ $t('about.cta.title') }}</h2>
            <p class="text-h6 mb-8">{{ $t('about.cta.description') }}</p>
            <div class="btn-group">
              <v-btn :to="localePath('/projects/submit')" color="green-bright" size="large" rounded="pill">
                {{ $t('about.cta.submitBtn') }}
              </v-btn>
              <v-btn :to="localePath('/contact')" variant="outlined" color="brown-dark" size="large" rounded="pill">
                {{ $t('about.cta.contactBtn') }}
              </v-btn>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
const localePath = useLocalePath()

useHead({
  title: t('about.meta.title')
})

const infoCards = [
  { icon: '🌱', title: 'about.info.established.label', value: 'about.info.established.value', detail: 'about.info.established.detail' },
  { icon: '🥐', title: 'about.info.location.label', value: 'about.info.location.value', detail: 'about.info.location.detail' },
  { icon: '🌍', title: 'about.info.reach.label', value: 'about.info.reach.value', detail: 'about.info.reach.detail' }
]

const methods = [
  { title: 'about.methodology.step1.title', description: 'about.methodology.step1.desc' },
  { title: 'about.methodology.step2.title', description: 'about.methodology.step2.desc' },
  { title: 'about.methodology.step3.title', description: 'about.methodology.step3.desc' },
  { title: 'about.methodology.step4.title', description: 'about.methodology.step4.desc' }
]

const values = [
  { icon: '🔓', title: 'about.values.open.title', description: 'about.values.open.desc' },
  { icon: '🤝', title: 'about.values.participatory.title', description: 'about.values.participatory.desc' },
  { icon: '🌐', title: 'about.values.global.title', description: 'about.values.global.desc' },
  { icon: '⚖️', title: 'about.values.ethical.title', description: 'about.values.ethical.desc' }
]
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.info-card {
  text-align: center;
  padding: $spacing-2xl;
  background: $surface-cream;
  border: 2px solid $border-cream;
  border-radius: $border-radius-md;

  .info-icon {
    font-size: 2.5rem;
    display: block;
    margin-bottom: $spacing-md;
  }

  h3 {
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: $green-dark;
    margin-bottom: $spacing-sm;
  }

  .info-number {
    font-size: 1.3rem;
    font-weight: 700;
    margin-bottom: $spacing-xs;
  }

  .info-detail {
    font-size: 0.95rem;
    opacity: 0.7;
  }
}

.method-card {
  background: $surface-cream;
  padding: $spacing-2xl;
  border: 2px solid $border-cream;
  text-align: center;
  border-radius: $border-radius-md;

  .method-number {
    font-size: 2.5rem;
    font-weight: 700;
    color: $green-bright;
    margin-bottom: $spacing-md;
  }
}

.value-card {
  padding: $spacing-2xl;

  .value-icon {
    font-size: 3rem;
  }
}
</style>
