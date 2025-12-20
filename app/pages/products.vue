<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" class="text-center mb-8">
        <h1 class="text-h2 mb-4">{{ $t('products.title') }}</h1>
        <p class="text-h6">{{ $t('products.subtitle') }}</p>
      </v-col>
    </v-row>

    <v-row>
      <v-col v-for="(product, i) in products" :key="i" cols="12" md="4">
        <v-card class="pillar-card h-100" elevation="0">
          <v-card-text>
            <div class="pillar-icon text-center mb-4">{{ product.icon }}</div>
            <h3 class="text-center mb-4">{{ $t(product.name) }}</h3>
            <p class="mb-4">{{ $t(product.description) }}</p>
            <div class="text-center">
              <v-btn
                :to="product.link"
                variant="outlined"
                color="green-bright"
                rounded="pill"
              >
                {{ $t('common.learnMore') }}
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: t('products.title')
})

const products = [
  { icon: '🤖', name: 'products.sleipnir.name', description: 'products.sleipnir.desc', link: '#' },
  { icon: '📊', name: 'products.database.name', description: 'products.database.desc', link: '/projects/database' },
  { icon: '📚', name: 'products.publications.name', description: 'products.publications.desc', link: '/resources/articles' }
]
</script>
