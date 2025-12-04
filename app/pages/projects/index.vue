<template>
  <div>
    <v-container class="py-16">
      <h1 class="text-h2 text-center mb-8">{{ $t('nav.projects') }}</h1>

      <!-- Filters -->
      <ProjectFilters
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
      <div class="text-center mb-4">
        <p class="text-body-1">
          {{ $t('projects.projectsFound', filteredProjects.length) }}
        </p>
      </div>

      <!-- Project list -->
      <v-row v-if="filteredProjects.length > 0">
        <v-col v-for="project in paginatedProjects" :key="project.pubId" cols="12" md="6" lg="4">
          <ProjectCard :project="project" @click="handleProjectClick" />
        </v-col>
      </v-row>

      <!-- Empty state -->
      <v-card v-else class="text-center pa-8">
        <v-icon size="64" color="grey-lighten-1">mdi-folder-open-outline</v-icon>
        <p class="text-h6 mt-4">{{ $t('projects.noProjects', 'No projects found') }}</p>
      </v-card>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="text-center mt-8">
        <v-pagination v-model="currentPage" :length="totalPages" :total-visible="7" />
      </div>
    </v-container>
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

// Country options for filter - get unique countries from all projects
const countryOptions = computed(() => {
  const countries = new Set<string>()
  projects.value.forEach((project) => {
    if (project.country && Array.isArray(project.country)) {
      project.country.forEach((c: string) => countries.add(c))
    }
  })
  return Array.from(countries)
    .sort()
    .map((code) => ({
      value: code,
      title: getCountryLabel(code)
    }))
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
    filtered = filtered.filter(
      (p) =>
        p.name?.toLowerCase().includes(query) ||
        p.description?.toLowerCase().includes(query) ||
        p.location?.toLowerCase().includes(query)
    )
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
