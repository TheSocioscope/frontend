<template>
  <v-container class="py-12">
    <h1 class="text-h2 mb-8 text-center">{{ $t('resources.articles.title') }}</h1>

    <v-row v-if="articles && articles.length > 0">
      <v-col v-for="article in articles" :key="article.id" cols="12" md="6">
        <v-card class="article-card" elevation="0">
          <v-card-text>
            <h3 class="mb-2">{{ article.title }}</h3>
            <p class="meta mb-2">{{ article.author }} • {{ article.date }}</p>
            <p>{{ article.excerpt }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn :href="article.link" variant="outlined" color="green-bright" rounded="pill">
              {{ $t('common.readMore') }}
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <div v-else class="text-center py-8">
      <p class="text-h6">{{ $t('resources.articles.comingSoon') }}</p>
    </div>
  </v-container>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: t('resources.articles.title')
})

const articles = ref([
  { id: 1, title: 'Understanding Food System Transformation', author: 'Research Team', date: '2024', excerpt: 'Key insights from our global research...', link: '#' },
  { id: 2, title: 'AI in Qualitative Research', author: 'Tech Team', date: '2024', excerpt: 'How we use LLMs to analyze patterns...', link: '#' }
])
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.article-card {
  border: 2px solid $border-cream;
  border-radius: $border-radius-lg;

  .meta {
    color: $green-bright;
    font-size: 0.9rem;
  }
}
</style>
