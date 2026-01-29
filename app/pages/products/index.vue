<template>
  <div>
    <ProductsHero />
    <section class="section">
      <div class="container">
        <ProductsIntro />
        <ProductsFilter :active-filter="activeFilter" @filter-change="handleFilterChange" />
        <ProductsGrid :products="products || []" :active-filter="activeFilter" />
      </div>
    </section>
    <ProductsCTA />
  </div>
</template>

<script setup lang="ts">
const { t, locale } = useI18n()

useHead({
  title: t('products.meta.title')
})

const activeFilter = ref('all')

const handleFilterChange = (filter: string) => {
  activeFilter.value = filter
}

// Fetch products from content
const { data: productsData } = await useAsyncData('products', () =>
  queryCollection('products').all()
)

const products = computed(() => {
  if (!productsData.value) return []
  const allProducts = Array.isArray(productsData.value) ? productsData.value : []
  return allProducts
    .filter((p: any) => p.published)
    .sort((a: any, b: any) => (a.order || 0) - (b.order || 0))
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section {
  padding: 5rem 0;
  background: $cream;

  @media (max-width: 768px) {
    padding: 4rem 0;
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}
</style>
