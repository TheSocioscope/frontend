<template>
  <section class="section partners-section">
    <v-container class="section-header">
      <h2>
        {{ $t('leadingResearch.title') }}
      </h2>

      <v-row justify="center">
        <v-col v-for="(partner, index) in displayedPartners" :key="index" cols="12" md="6">
          <v-card
            class="partner-card"
            elevation="2"
            :href="partner.url"
            target="_blank"
            rel="noopener noreferrer"
          >
            <v-card-text class="text-center pa-8">
              <h4 class="text-h5 font-weight-medium mb-4">{{ partner.title }}</h4>
              <p class="text-body-2">{{ partner.lead }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <p class="text-body-1 font-italic text-center mt-8 nomis-support">
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
    lead: 'Helga Nowotny, Project Lead',
    url: 'https://csh.ac.at/'
  },
  {
    title: 'Paris Institute for Advanced Study',
    lead: 'Saadi Lahlou, Project Lead',
    url: 'https://www.paris-iea.fr/en'
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
      lead: p.lead,
      url: p.url
    }))
  }
  return fallbackPartners
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.partners-section {
  background: $surface-cream;
}

.partner-card {
  background: white;
  height: 100%;

  h4 {
    color: $green-bright;
    font-family: $font-family-display;
  }

  p {
    color: $brown-dark;
    line-height: 1.6;
    font-family: $font-family-display;
  }
}

.nomis-support {
  color: $brown-medium;
}
</style>
