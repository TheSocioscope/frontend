<template>
  <div>
    <PageHero
      :title="$t('products.hero.title')"
      :subtitle="$t('products.hero.subtitle')"
      icon="🛒"
    />
    <section class="section">
      <div class="container">
        <ProductsIntro />
        <ProductsFilter :active-filter="activeFilter" @filter-change="handleFilterChange" />

        <!-- Sort and Per Page Controls with Reset Button -->
        <ListControls
          v-model:sort-by="sortBy"
          v-model:sort-order="sortOrder"
          v-model:items-per-page="itemsPerPage"
          :sort-options="sortOptions"
          :sort-label="$t('products.sortBy')"
          :per-page-label="$t('products.perPage')"
          :show-per-page="!isMobile"
        >
          <template #center>
            <ListFilterResetButton :has-active-filters="hasActiveFilters" @reset="resetFilters" />
          </template>
        </ListControls>

        <!-- Desktop: Paginated Grid -->
        <ProductsGrid v-if="!isMobile" :products="items" :active-filter="activeFilter" />

        <!-- Mobile: Lazy Loading Grid -->
        <ProductsGrid v-else :products="displayedItems" :active-filter="activeFilter" />

        <!-- Desktop Pagination -->
        <ListPagination
          v-if="!isMobile && totalPages > 1"
          :current-page="currentPage"
          :total-pages="totalPages"
          :previous-label="$t('products.pagination.previous')"
          :next-label="$t('products.pagination.next')"
          @prev="prevPage"
          @next="nextPage"
          @goto="goToPage"
        />

        <!-- Mobile Load More -->
        <ListLoadMore
          v-if="isMobile"
          :has-more="hasMore"
          :label="$t('products.loadMore')"
          @load-more="loadMore"
        />

        <!-- Results Count -->
        <ListResultsInfo
          :start="isMobile ? 1 : (currentPage - 1) * itemsPerPage + 1"
          :end="isMobile ? displayedItems.length : Math.min(currentPage * itemsPerPage, totalItems)"
          :total="totalItems"
          :message="
            $t('products.showing', {
              start: isMobile ? 1 : (currentPage - 1) * itemsPerPage + 1,
              end: isMobile
                ? displayedItems.length
                : Math.min(currentPage * itemsPerPage, totalItems),
              total: totalItems
            })
          "
        />
      </div>
    </section>
    <ProductsCTA />
  </div>
</template>

<script setup lang="ts">
const { t, t: $t } = useI18n()

useHead({
  title: t('products.meta.title')
})

const activeFilter = ref('all')
const isMobile = ref(false)

const sortOptions = [
  { value: 'order', label: $t('products.sort.order') },
  { value: 'title', label: $t('products.sort.name') },
  { value: 'publishedAt', label: $t('products.sort.dateAdded') }
]

// Detect mobile/desktop
onMounted(() => {
  isMobile.value = window.innerWidth < 768
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth < 768
  })
})

const handleFilterChange = (filter: string) => {
  activeFilter.value = filter
}

// Check if any filters are active (not 'all')
const hasActiveFilters = computed(() => {
  return activeFilter.value !== 'all'
})

const resetFilters = () => {
  activeFilter.value = 'all'
}

// Use the localized collection composable
const {
  items,
  currentPage,
  totalItems,
  totalPages,
  itemsPerPage,
  goToPage,
  nextPage,
  prevPage,
  hasNextPage,
  hasPrevPage,
  sortBy,
  sortOrder,
  displayedItems,
  loadMore,
  hasMore
} = useLocalizedCollection('products', {
  itemsPerPage: 20,
  sortBy: 'order',
  sortOrder: 'asc'
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
