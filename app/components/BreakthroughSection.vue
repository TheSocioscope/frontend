<template>
  <section class="section breakthrough-section">
    <v-container>
      <h2 class="section-title text-center">
        {{ $t('breakthroughs.title') }}
      </h2>
      <p class="breakthrough-subtitle text-center">
        {{ $t('breakthroughs.subtitle') }}
      </p>

      <v-row>
        <v-col v-for="(card, index) in breakthroughs" :key="index" cols="12" md="6">
          <v-card
            class="breakthrough-card h-100"
            elevation="2"
            :to="card._path ? localePath(card._path) : undefined"
          >
            <v-card-text>
              <h4 class="mb-4">{{ card.title }}</h4>
              <p>{{ card.description }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t, locale } = useI18n()
const localePath = useLocalePath()

// Fallback breakthrough cards from i18n
const fallbackBreakthroughs = [
  {
    title: $t('breakthroughs.card1.title'),
    description: $t('breakthroughs.card1.description')
  },
  {
    title: $t('breakthroughs.card2.title'),
    description: $t('breakthroughs.card2.description')
  },
  {
    title: $t('breakthroughs.card3.title'),
    description: $t('breakthroughs.card3.description')
  },
  {
    title: $t('breakthroughs.card4.title'),
    description: $t('breakthroughs.card4.description')
  }
]

// Fetch breakthrough cards from content
const { data: contentCards } = await useAsyncData(
  'scientific-breakthroughs',
  async () => {
    try {
      const content = await queryContent(`pages/${locale.value}/scientific-breakthroughs`)
        .where({ published: true })
        .find()
      return content
    } catch (e) {
      return null
    }
  },
  { watch: [locale], default: () => null }
)

// Use content or fallback to i18n
const breakthroughs = computed(() => {
  if (contentCards.value && contentCards.value.length > 0) {
    return contentCards.value
  }

  return fallbackBreakthroughs
})
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.breakthrough-section {
  background: white;
}

.breakthrough-title {
  margin-bottom: $spacing-3xl;
}

.breakthrough-grid {
  font-size: 1.3rem;
  color: $brown-dark;
  max-width: 900px;
  margin: 0 auto $spacing-3xl;
  line-height: 1.7;

  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
}

.breakthrough-card {
  background: $surface-cream;
  transition:
    transform $transition-base,
    box-shadow $transition-base;

  &:hover {
    transform: translateY(-5px);
    box-shadow: $shadow-lg !important;
  }

  h4 {
    font-size: 1.8rem;
    color: $brown-medium;
    font-weight: 500;
  }

  p {
    font-size: 1.1rem;
    color: $brown-dark;
    line-height: 1.7;
  }
}
</style>
