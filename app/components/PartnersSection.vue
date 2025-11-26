<template>
  <section class="section partners-section">
    <v-container>
      <h2 class="section-title text-center mb-12">{{ $t('leadingResearch.title') }}</h2>

      <v-row justify="center">
        <v-col v-for="(partner, index) in displayedPartners" :key="index" cols="12" md="6">
          <v-card class="partner-card" elevation="2">
            <v-card-text class="text-center pa-8">
              <h4 class="mb-4">{{ partner.title }}</h4>
              <p>{{ partner.lead }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <p class="nomis-support text-center mt-8">
        {{ $t('leadingResearch.nomis') }}
      </p>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t, locale } = useI18n()

// Fallback partners from i18n
const fallbackPartners = [
  {
    title: 'Complexity Science Hub Vienna',
    lead: 'Helga Nowotny, Project Lead'
  },
  {
    title: 'Paris Institute for Advanced Study',
    lead: 'Saadi Lahlou, Project Lead'
  }
]

// Fetch partners from content
const { data: partners } = await useAsyncData(
  'partners',
  async () => {
    try {
      const content = await queryContent(`partners/${locale.value}`)
        .where({ published: true })
        .sort({ order: 1 })
        .find()
      return content
    } catch (e) {
      return null
    }
  },
  { watch: [locale], default: () => null }
)

const displayedPartners = computed(() => {
  if (partners.value && Array.isArray(partners.value) && partners.value.length > 0) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return partners.value.map((p: any) => ({
      title: p.title,
      lead: p.lead
    }))
  }
  return fallbackPartners
})
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.partners-section {
  background: $surface-cream;
}

h2 {
  font-size: 3rem;
  color: $brown-medium;
  font-weight: 400;

  @media (max-width: 768px) {
    font-size: 2rem;
  }
}

.partner-card {
  background: white;
  height: 100%;

  h4 {
    font-size: 1.4rem;
    color: $brown-medium;
    font-weight: 500;
  }

  p {
    color: $brown-dark;
    font-size: 1.1rem;
    line-height: 1.6;
  }
}

.nomis-support {
  font-size: 1.2rem;
  color: $brown-medium;
  font-style: italic;

  @media (max-width: 768px) {
    font-size: 1rem;
  }
}
</style>
