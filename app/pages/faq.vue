<template>
  <div class="faq-page">
    <!-- Hero Section -->
    <PageHero :title="$t('faq.title')" :subtitle="$t('faq.subtitle')" icon="❓" />

    <!-- FAQ Section -->
    <section class="section">
      <div class="container">
        <div class="faq-container">
          <!-- Category Filter Chips -->
          <div class="category-nav">
            <v-chip
              :variant="selectedCategory === null ? 'flat' : 'outlined'"
              :color="selectedCategory === null ? 'green-bright' : undefined"
              class="category-chip"
              @click="selectedCategory = null"
            >
              {{ $t('faq.allCategories') }}
            </v-chip>
            <v-chip
              v-for="category in categories"
              :key="category"
              :variant="selectedCategory === category ? 'flat' : 'outlined'"
              :color="selectedCategory === category ? 'green-bright' : undefined"
              class="category-chip"
              @click="selectedCategory = category"
            >
              {{ $t(`faq.categories.${category}`) }}
            </v-chip>
          </div>

          <!-- FAQ Items -->
          <div v-if="filteredFaqItems && filteredFaqItems.length > 0">
            <!-- Grouped by category when showing all -->
            <template v-if="selectedCategory === null">
              <div v-for="category in categories" :key="category" class="faq-category">
                <h2 class="faq-category-title">{{ $t(`faq.categories.${category}`) }}</h2>
                <v-expansion-panels v-model="expandedPanel">
                  <v-expansion-panel
                    v-for="(item, index) in getItemsByCategory(category)"
                    :key="index"
                    :value="getCategoryItemIndex(category, index)"
                    class="faq-item"
                  >
                    <v-expansion-panel-title class="faq-question">
                      <span class="faq-question-text">{{ item.question }}</span>
                    </v-expansion-panel-title>
                    <v-expansion-panel-text class="faq-answer">
                      <ContentRenderer :value="item" class="faq-answer-content" />
                    </v-expansion-panel-text>
                  </v-expansion-panel>
                </v-expansion-panels>
              </div>
            </template>

            <!-- Single category view -->
            <template v-else>
              <v-expansion-panels v-model="expandedPanel">
                <v-expansion-panel
                  v-for="(item, index) in filteredFaqItems"
                  :key="index"
                  :value="index"
                  class="faq-item"
                >
                  <v-expansion-panel-title class="faq-question">
                    <span class="faq-question-text">{{ item.question }}</span>
                  </v-expansion-panel-title>
                  <v-expansion-panel-text class="faq-answer">
                    <ContentRenderer :value="item" class="faq-answer-content" />
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </template>
          </div>

          <div v-else class="text-center py-8">
            <p class="text-h6">{{ $t('faq.comingSoon') }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="section cta-section">
      <div class="container">
        <div class="cta-content">
          <h2>{{ $t('faq.stillHaveQuestions') }}</h2>
          <p>{{ $t('faq.contactPrompt') }}</p>
          <div class="btn-group">
            <NuxtLink :to="localePath('/contact')" class="btn btn-primary">
              {{ $t('nav.contactUs') }}
            </NuxtLink>
            <NuxtLink :to="localePath('/projects')" class="btn btn-outline">
              {{ $t('faq.exploreDatabase') }}
            </NuxtLink>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
interface FaqItem {
  question: string
  order: number
  category?: string
  body?: unknown
  _path?: string
}

const { t, locale } = useI18n()
const localePath = useLocalePath()

useHead({
  title: t('faq.title')
})

const selectedCategory = ref<string | null>(null)
// Single model for all expansion panels (source of truth)
const expandedPanel = ref<number | undefined>(undefined)

const { data: faqItems } = await useAsyncData<FaqItem[]>(
  `faq-${locale.value}`,
  async () => {
    try {
      const allFaqs = await queryCollection('faq').all()
      console.log('All FAQs loaded:', allFaqs.length)
      console.log('Current locale:', locale.value)

      // Filter by checking if the _path contains the locale folder
      const localizedFaqs = allFaqs
        .filter((item: any) => {
          // Check if _path contains /faq/{locale}/
          const pathMatch =
            item._path?.includes(`/faq/${locale.value}/`) ||
            item._path?.includes(`faq/${locale.value}/`) ||
            item.stem?.includes(`faq/${locale.value}/`)
          return pathMatch
        })
        .sort((a: any, b: any) => (a.order || 0) - (b.order || 0))

      console.log('Localized FAQs:', localizedFaqs.length)

      if (localizedFaqs.length > 0) return localizedFaqs

      // Fallback to English if no items in current locale
      const englishFaqs = allFaqs
        .filter((item: any) => {
          const pathMatch =
            item._path?.includes('/faq/en/') ||
            item._path?.includes('faq/en/') ||
            item.stem?.includes('faq/en/')
          return pathMatch
        })
        .sort((a: any, b: any) => (a.order || 0) - (b.order || 0))

      console.log('English FAQs (fallback):', englishFaqs.length)
      return englishFaqs
    } catch (e) {
      console.error('Error loading FAQ items:', e)
      return []
    }
  },
  { watch: [locale] }
)

// Get unique categories from FAQ items
const categories = computed(() => {
  if (!faqItems.value) return []
  const cats = new Set<string>()
  faqItems.value.forEach((item) => {
    if (item.category) cats.add(item.category)
  })
  return Array.from(cats).sort()
})

// Filter FAQ items by selected category
const filteredFaqItems = computed(() => {
  if (!faqItems.value) return []
  if (selectedCategory.value === null) return faqItems.value
  return faqItems.value.filter((item) => item.category === selectedCategory.value)
})

// Helper to get items by category for grouped display
const getItemsByCategory = (category: string) => {
  if (!faqItems.value) return []
  return faqItems.value.filter((item) => item.category === category)
}

// Helper to get the global index of an item within a category
const getCategoryItemIndex = (category: string, localIndex: number) => {
  if (!faqItems.value) return localIndex

  // Calculate the global index by counting all items before this category
  let globalIndex = 0
  for (const cat of categories.value) {
    if (cat === category) {
      return globalIndex + localIndex
    }
    globalIndex += getItemsByCategory(cat).length
  }
  return localIndex
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.faq-page {
  font-family: 'Playfair Display', serif;
  background-color: $cream;
  color: $brown-dark;
}

/* Section */
.section {
  padding: 5rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* FAQ Container */
.faq-container {
  max-width: 900px;
  margin: 0 auto;
}

/* FAQ Category */
.faq-category {
  margin-bottom: 3rem;
}

.faq-category-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: $forest-green;
  text-align: center;
  font-weight: 700;
}

/* Category Navigation */
.category-nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 4rem;
}

.category-chip {
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 0 !important;

  :deep(.v-chip__content) {
    font-family: 'Playfair Display', serif;
  }
}

/* FAQ Items */
.faq-item {
  background: white;
  border: 2px solid $warm-beige;
  margin-bottom: 1rem;
  transition: all 0.3s ease;

  &:deep(.v-expansion-panel-title) {
    padding: 1.5rem 2rem;
    font-family: 'Playfair Display', serif;
    transition: all 0.3s ease;

    &:hover {
      background: $warm-beige;
    }
  }

  &:deep(.v-expansion-panel-title--active) {
    border-bottom: 2px solid $warm-beige;
  }
}

.faq-question-text {
  font-size: 1.15rem;
  font-weight: 600;
  color: $brown-dark;
  font-family: 'Playfair Display', serif;
}

.faq-answer {
  :deep(.v-expansion-panel-text__wrapper) {
    padding: 1.5rem 2rem 1.5rem 2rem;
  }
}

.faq-answer-content {
  font-size: 1.05rem;
  line-height: 1.8;
  color: $brown-dark;
  opacity: 0.85;
  font-family: 'Playfair Display', serif;

  :deep(p) {
    margin-bottom: 1rem;
  }

  :deep(strong) {
    font-weight: 600;
    color: $forest-green;
  }

  :deep(ul) {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
  }

  :deep(li) {
    margin-bottom: 0.5rem;
  }
}

/* CTA Section */
.cta-section {
  background: $warm-beige;
  text-align: center;
  border-top: 3px solid $green-bright;
}

.cta-content {
  max-width: 700px;
  margin: 0 auto;

  h2 {
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    color: $brown-dark;
    font-weight: 700;
  }

  p {
    font-size: 1.2rem;
    margin-bottom: 2.5rem;
    color: $brown-dark;
    line-height: 1.7;
  }
}

.btn-group {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  display: inline-block;
  padding: 1rem 2.5rem;
  font-weight: 600;
  text-decoration: none;
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  border-radius: 0;
}

.btn-primary {
  background: $green-bright;
  color: white;
  border-color: $green-bright;

  &:hover {
    background: $forest-green;
    border-color: $forest-green;
  }
}

.btn-outline {
  background: transparent;
  color: $brown-dark;
  border-color: $brown-dark;

  &:hover {
    background: $brown-dark;
    color: $cream;
  }
}

/* Responsive Design */
@media (max-width: 768px) {
  .section {
    padding: 4rem 0;
  }

  .category-nav {
    gap: 0.75rem;
  }

  .btn-group {
    flex-direction: column;

    .btn {
      width: 100%;
      text-align: center;
    }
  }
}
</style>
