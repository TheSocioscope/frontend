<template>
  <div>
    <ProjectsHero />
    <section class="section">
      <div class="container">
        <!-- Filters -->
        <ProjectsFilters
          :filters="filters"
          :continent-options="continentOptions"
          :country-options="countryOptions"
          :status-options="statusOptions"
          :thematic-options="thematicOptions"
          :field-options="fieldOptions"
          :type-options="typeOptions"
          class="mb-8"
          @update:model-value="filters = $event"
        />

        <!-- Results count -->
        <div class="results-info">
          <p>
            {{ $t('projects.projectsFound', filteredProjects.length) }}
          </p>
        </div>

        <!-- Project list -->
        <div v-if="filteredProjects.length > 0" class="projects-grid">
          <ProjectsCard
            v-for="project in paginatedProjects"
            :key="project.pubId"
            :project="project"
            @click="handleProjectClick"
          />
        </div>

        <!-- Empty state -->
        <div v-else class="empty-state">
          <p>{{ $t('projects.noProjects', 'No projects found') }}</p>
        </div>

        <!-- Pagination -->
        <div v-if="totalPages > 1" class="pagination-container">
          <v-pagination v-model="currentPage" :length="totalPages" :total-visible="7" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const localePath = useLocalePath()
const route = useRoute()
const router = useRouter()
const {
  getContinentLabel,
  getCountryLabel,
  getThematicLabel,
  getFieldLabel,
  getTypeLabel,
  getStatusLabel
} = useProjectMappings()

// Fetch all projects
const { data: projectsData } = await useAsyncData('projects', () =>
  queryCollection('projects').all()
)

const projects = computed(() => {
  if (!projectsData.value) return []
  return Array.isArray(projectsData.value) ? projectsData.value : []
})

// Filter state
const filters = ref({
  searchQuery: '',
  selectedContinent: null as string | null,
  selectedCountries: [] as string[],
  selectedStatus: null as string | null,
  selectedThematics: [] as string[],
  selectedFields: [] as string[],
  selectedTypes: [] as string[]
})

const currentPage = ref(1)
const itemsPerPage = 12

// Initialize filters from URL query
onMounted(() => {
  const { countries, continent, status, thematics, fields, types } = route.query

  if (countries) {
    filters.value.selectedCountries = Array.isArray(countries) ? countries : [countries as string]
  }
  if (continent) filters.value.selectedContinent = continent as string
  if (status) filters.value.selectedStatus = status as string
  if (thematics) {
    filters.value.selectedThematics = Array.isArray(thematics) ? thematics : [thematics as string]
  }
  if (fields) {
    filters.value.selectedFields = Array.isArray(fields) ? fields : [fields as string]
  }
  if (types) {
    filters.value.selectedTypes = Array.isArray(types) ? types : [types as string]
  }
})

// Update URL when filters change
watch(
  filters,
  () => {
    const query: Record<string, string | string[]> = {}

    if (filters.value.selectedCountries.length) query.countries = filters.value.selectedCountries
    if (filters.value.selectedContinent) query.continent = filters.value.selectedContinent
    if (filters.value.selectedStatus) query.status = filters.value.selectedStatus
    if (filters.value.selectedThematics.length) query.thematics = filters.value.selectedThematics
    if (filters.value.selectedFields.length) query.fields = filters.value.selectedFields
    if (filters.value.selectedTypes.length) query.types = filters.value.selectedTypes

    router.push({ query })
  },
  { deep: true }
)

// Continent options for filter
const continentOptions = computed(() => {
  return [
    { value: 'asia', title: getContinentLabel('asia') },
    { value: 'europe', title: getContinentLabel('europe') },
    { value: 'north-africa', title: getContinentLabel('north-africa') },
    { value: 'north-america', title: getContinentLabel('north-america') },
    { value: 'south-america', title: getContinentLabel('south-america') },
    { value: 'sub-saharian-africa', title: getContinentLabel('sub-saharian-africa') },
    { value: 'oceania', title: getContinentLabel('oceania') },
    { value: 'worldwide-intercontinental', title: getContinentLabel('worldwide-intercontinental') }
  ]
})

// Country options for filter - get unique countries from all projects with translations
const countryOptions = computed(() => {
  const countries = new Set<string>()
  projects.value.forEach((project) => {
    if (project.country && Array.isArray(project.country)) {
      project.country.forEach((c: string) => countries.add(c))
    }
  })
  return Array.from(countries)
    .map((code) => ({
      value: code,
      title: getCountryLabel(code)
    }))
    .filter((option) => option.title !== option.value) // Only show countries with translations
    .sort((a, b) => a.title.localeCompare(b.title))
})

// Status options for filter
const statusOptions = computed(() => {
  return [
    { value: 'pending', title: getStatusLabel('pending') },
    { value: 'published', title: getStatusLabel('published') },
    { value: 'stale', title: getStatusLabel('stale') },
    { value: 'verified', title: getStatusLabel('verified') },
    { value: 'new', title: getStatusLabel('new') }
  ]
})

// Get unique options from projects
const getUniqueOptions = (field: string, labelFn: (code: string) => string) => {
  const items = new Set<string>()
  projects.value.forEach((project) => {
    const values = project[field]
    if (values && Array.isArray(values)) {
      values.forEach((v: string) => items.add(v))
    }
  })
  return Array.from(items)
    .sort()
    .map((code) => ({ value: code, title: labelFn(code) }))
}

const thematicOptions = computed(() => getUniqueOptions('thematic', getThematicLabel))
const fieldOptions = computed(() => getUniqueOptions('field', getFieldLabel))
const typeOptions = computed(() => getUniqueOptions('type', getTypeLabel))

// Filtered projects
const filteredProjects = computed(() => {
  let filtered = projects.value.filter((p) => !p.removedAt)

  const {
    searchQuery,
    selectedContinent,
    selectedCountries,
    selectedStatus,
    selectedThematics,
    selectedFields,
    selectedTypes
  } = filters.value

  if (searchQuery) {
    const query = searchQuery.toLowerCase()
    filtered = filtered.filter((p) => {
      // Helper function to get searchable text from multilingual fields
      const getSearchableText = (field: any): string => {
        if (!field) return ''
        if (typeof field === 'string') return field.toLowerCase()
        if (typeof field === 'object') {
          return Object.values(field)
            .filter((v) => typeof v === 'string')
            .join(' ')
            .toLowerCase()
        }
        return ''
      }

      const searchableName = getSearchableText(p.name)
      const searchableDescription = getSearchableText(p.description)
      const searchableLocation = p.location?.toLowerCase() || ''

      return (
        searchableName.includes(query) ||
        searchableDescription.includes(query) ||
        searchableLocation.includes(query)
      )
    })
  }

  if (selectedContinent) {
    filtered = filtered.filter((p) => p.continent?.includes(selectedContinent))
  }

  if (selectedCountries.length) {
    filtered = filtered.filter((p) => p.country?.some((c: string) => selectedCountries.includes(c)))
  }

  if (selectedStatus) {
    filtered = filtered.filter((p) => p.status === selectedStatus)
  }

  if (selectedThematics.length) {
    filtered = filtered.filter((p) =>
      p.thematic?.some((t: string) => selectedThematics.includes(t))
    )
  }

  if (selectedFields.length) {
    filtered = filtered.filter((p) => p.field?.some((f: string) => selectedFields.includes(f)))
  }

  if (selectedTypes.length) {
    filtered = filtered.filter((p) => p.type?.some((t: string) => selectedTypes.includes(t)))
  }

  return filtered.sort((a, b) => (b.score || 0) - (a.score || 0))
})

// Pagination
const totalPages = computed(() => Math.ceil(filteredProjects.value.length / itemsPerPage))

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredProjects.value.slice(start, end)
})

// Reset page when filters change
watch(
  filters,
  () => {
    currentPage.value = 1
  },
  { deep: true }
)

// Navigation handler
const handleProjectClick = (project: { stem: string }) => {
  const projectId = project.stem.replace('projects/', '')
  navigateTo(localePath(`/projects/${projectId}`))
}

useHead({
  title: $t('nav.projects')
})
</script>

<style scoped lang="scss">
.section {
  padding: 4rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin: 2rem 0;
}

.results-info {
  text-align: center;
  margin: 2rem 0;
  color: #666;
  font-size: 1.1rem;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #666;

  h2 {
    font-size: 1.5rem;
    margin-bottom: 1rem;
    color: #333;
  }

  p {
    font-size: 1.1rem;
  }
}

.pagination-container {
  display: flex;
  justify-content: center;
  margin: 3rem 0;
}
</style>
