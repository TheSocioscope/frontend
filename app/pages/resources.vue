<template>
  <div>
    <ResourcesHero @submit="openModal" />
    <section class="section" id="resources">
      <div class="container">
        <ResourcesSearch
          :active-filter="activeFilter"
          :search-query="searchQuery"
          @filter-change="handleFilterChange"
          @search-change="handleSearchChange"
        />
        <ResourcesGrid
          :resources="resources || []"
          :active-filter="activeFilter"
          :search-query="searchQuery"
        />
      </div>
    </section>
    <ResourcesCTA @submit="openModal" />
    <ResourcesSubmitModal :is-open="isModalOpen" @close="closeModal" />
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()
const route = useRoute()

useHead({
  title: t('resources.meta.title')
})

const activeFilter = ref('all')
const searchQuery = ref('')
const isModalOpen = ref(false)

const validFilters = ['article', 'book', 'event', 'funding', 'organization', 'policy', 'socioscope']

// Apply filter from URL query parameter
const updateFilterFromRoute = () => {
  const filterParam = route.query.filter
  if (filterParam && typeof filterParam === 'string' && validFilters.includes(filterParam)) {
    activeFilter.value = filterParam
  } else {
    activeFilter.value = 'all'
  }
}

// Initialize filter from URL on mount
onMounted(() => {
  updateFilterFromRoute()
})

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

const openModal = () => {
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
}

// Fetch resources from content
const { data: resourcesData } = await useAsyncData('resources', () =>
  queryCollection('resources').all()
)

console.log('=== RESOURCES DEBUG ===')
console.log('resourcesData:', resourcesData.value)
console.log('Is array?', Array.isArray(resourcesData.value))
console.log('Length:', resourcesData.value?.length)
console.log('First item:', resourcesData.value?.[0])

const resources = computed(() => {
  if (!resourcesData.value) {
    console.log('No resourcesData')
    return []
  }
  const allResources = Array.isArray(resourcesData.value) ? resourcesData.value : []
  console.log('All resources count:', allResources.length)
  const filtered = allResources.filter((r: any) => r.published !== false)
  console.log('Published resources count:', filtered.length)
  return filtered.sort((a: any, b: any) => (a.order || 0) - (b.order || 0))
})
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

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
