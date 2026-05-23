<template>
  <div>
    <PageHero
      :title="$t('resources.hero.title')"
      :subtitle="$t('resources.hero.subtitle')"
      icon="mdi-bookshelf"
      compact
      centered
    >
      <template #cta>
        <div class="hero-cta">
          <a href="mailto:info@thesocioscope.org" class="submit-cta">
            <v-icon size="small">mdi-plus-circle-outline</v-icon>
            <span>{{ $t('resources.hero.submitCta') }}</span>
            <v-icon size="small" class="cta-arrow">mdi-arrow-right</v-icon>
          </a>
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
          class="section-reveal"
        />

        <!-- Mobile: Lazy Loading Grid -->
        <ResourcesGrid
          v-else
          :resources="displayedItems || []"
          :active-filter="activeFilter"
          :search-query="searchQuery"
          class="section-reveal"
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
    <!--<ResourcesSubmitModal :is-open="isModalOpen" @close="closeModal" />-->
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

/* Hero CTA — centered, sleek pill button matching the site's arrow-chip
   vocabulary. Centered both visually (text-align) and structurally
   (margin: 0 auto on the link itself). */
.hero-cta {
  display: flex;
  justify-content: center;
  margin-top: 1.25rem;

  @media (max-width: 768px) {
    margin-top: 1rem;
  }
}

.submit-cta {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem 0.625rem 1.125rem;
  background: white;
  border: 1px solid rgba(44, 36, 22, 0.2);
  border-radius: 999px;
  color: $brown-dark;
  font-family: $font-family-display;
  font-size: 0.9375rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;

  .cta-arrow {
    transition: transform 0.2s ease;
  }

  &:hover,
  &:focus-visible {
    background: $green-bright;
    color: white;
    border-color: $green-bright;
    transform: translateY(-2px);

    .cta-arrow {
      transform: translateX(2px);
    }
  }

  &:focus-visible {
    outline: 2px solid $green-bright;
    outline-offset: 2px;
  }
}

.section {
  padding: 2.5rem 0 3rem;
  background: $cream;

  @media (max-width: 768px) {
    padding: 2rem 0 2.5rem;
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;

  @media (max-width: 768px) {
    padding: 0 1rem;
  }
}
</style>
