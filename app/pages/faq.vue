<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <h1 class="text-h2 mb-8">{{ $t('pages.faq') }}</h1>

        <v-expansion-panels v-if="faqItems && faqItems.length > 0">
          <v-expansion-panel v-for="(item, index) in faqItems" :key="index">
            <v-expansion-panel-title>
              <strong>{{ item.question }}</strong>
            </v-expansion-panel-title>
            <v-expansion-panel-text>
              <ContentRenderer :value="item" />
            </v-expansion-panel-text>
          </v-expansion-panel>
        </v-expansion-panels>

        <div v-else class="text-center py-8">
          <p class="text-h6">{{ $t('pages.faq') }} coming soon...</p>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
interface FaqItem {
  question: string
  order: number
  body?: unknown
  _path?: string
}

const { t, locale } = useI18n()

useHead({
  title: t('pages.faq')
})

// Load FAQ items from content based on current locale
const { data: faqItems } = await useAsyncData<FaqItem[]>(
  `faq-${locale.value}`,
  async () => {
    try {
      const items = await queryContent<FaqItem>(`faq/${locale.value}`).sort({ order: 1 }).find()
      return items
    } catch {
      // Fallback to English if locale content not found
      try {
        const items = await queryContent<FaqItem>('faq/en').sort({ order: 1 }).find()
        return items
      } catch {
        return []
      }
    }
  },
  { watch: [locale] }
)
</script>
