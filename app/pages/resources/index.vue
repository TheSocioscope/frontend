<template>
  <div>
    <PageHero
      :title="$t('resources.hero.title')"
      :subtitle="$t('resources.hero.subtitle')"
      icon="📚"
    >
      <template #cta>
        <div class="hero-cta">
          <a href="#resources" class="btn">{{ $t('resources.hero.browseCta') }}</a>
          <button class="btn btn-secondary" @click="openModal">
            {{ $t('resources.hero.submitCta') }}
          </button>
        </div>
      </template>
    </PageHero>
    <section id="resources" class="section">
      <div class="container">
        <ResourcesSearch
          :active-filter="activeFilter"
          :search-query="searchQuery"
          @filter-change="handleFilterChange"
          @search-change="handleSearchChange"
        />

        <!-- Sort and Per Page Controls with Reset Button -->
        <ListControls
          v-model:sort-by="sortBy"
          v-model:sort-order="sortOrder"
          v-model:items-per-page="itemsPerPage"
          :sort-options="sortOptions"
          :sort-label="$t('resources.sortBy')"
          :per-page-label="$t('resources.perPage')"
          :show-per-page="!isMobile"
        >
          <template #center>
            <ListFilterResetButton :has-active-filters="hasActiveFilters" @reset="resetFilters" />
          </template>
        </ListControls>

        <!-- Desktop: Paginated Grid -->
        <ResourcesGrid
          v-if="!isMobile"
          :resources="items || []"
          :active-filter="activeFilter"
          :search-query="searchQuery"
        />

        <!-- Mobile: Lazy Loading Grid -->
        <ResourcesGrid
          v-else
          :resources="displayedItems || []"
          :active-filter="activeFilter"
          :search-query="searchQuery"
        />

        <!-- Desktop Pagination -->
        <ListPagination
          v-if="!isMobile && totalPages > 1"
          :current-page="currentPage"
          :total-pages="totalPages"
          :previous-label="$t('resources.pagination.previous')"
          :next-label="$t('resources.pagination.next')"
          @prev="prevPage"
          @next="nextPage"
          @goto="goToPage"
        />

        <!-- Mobile Load More -->
        <ListLoadMore
          v-if="isMobile"
          :has-more="hasMore"
          :label="$t('resources.loadMore')"
          @load-more="loadMore"
        />

        <!-- Results Count -->
        <ListResultsInfo
          :start="isMobile ? 1 : (currentPage - 1) * itemsPerPage + 1"
          :end="isMobile ? displayedItems.length : Math.min(currentPage * itemsPerPage, totalItems)"
          :total="totalItems"
          :message="
            $t('resources.showing', {
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
    <ResourcesSubmitModal :is-open="isModalOpen" @close="closeModal" />
  </div>
</template>

<script setup lang="ts">
const { t, t: $t } = useI18n()
const route = useRoute()

useHead({
  title: t('resources.meta.title')
})

const activeFilter = ref('all')
const searchQuery = ref('')
const isModalOpen = ref(false)
const isMobile = ref(false)

const validFilters = ['article', 'book', 'event', 'funding', 'organization', 'policy', 'socioscope']

const sortOptions = [
  { value: 'createdAt', label: $t('resources.sort.date') },
  { value: 'title', label: $t('resources.sort.name') }
]

// Detect mobile/desktop
onMounted(() => {
  isMobile.value = window.innerWidth < 768
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth < 768
  })
  updateFilterFromRoute()
})

// Apply filter from URL query parameter
const updateFilterFromRoute = () => {
  const filterParam = route.query.filter
  if (filterParam && typeof filterParam === 'string' && validFilters.includes(filterParam)) {
    activeFilter.value = filterParam
  } else {
    activeFilter.value = 'all'
  }
}

// Watch for route query changes and update filter
watch(
  () => route.query.filter,
  () => {
    updateFilterFromRoute()
  }
)

const handleFilterChange = (filter: string) => {
  activeFilter.value = filter
}

const handleSearchChange = (query: string) => {
  searchQuery.value = query
}

// Check if any filters are active (not 'all' or has search query)
const hasActiveFilters = computed(() => {
  return activeFilter.value !== 'all' || searchQuery.value.trim() !== ''
})

const resetFilters = () => {
  activeFilter.value = 'all'
  searchQuery.value = ''
}

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
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
  sortBy,
  sortOrder,
  displayedItems,
  loadMore,
  hasMore
} = useLocalizedCollection('resources', {
  itemsPerPage: 20,
  sortBy: 'createdAt',
  sortOrder: 'desc'
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.hero-cta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 2rem;
}

.btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 0;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
  background: $green-bright;
  color: white;
  border: none;
  cursor: pointer;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.btn-secondary {
  background: transparent;
  color: $brown-dark;
  border: 2px solid $brown-dark;

  &:hover {
    background: $brown-dark;
    color: white;
  }
}

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
