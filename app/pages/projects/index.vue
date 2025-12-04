<template>
  <div>
    <v-container class="py-16">
      <h1 class="text-h2 text-center mb-8">{{ $t('nav.projects') }}</h1>

      <!-- Filters -->
      <v-card class="mb-8">
        <v-card-text>
          <v-row>
            <!-- Row 1 -->
            <v-col cols="12" md="4">
              <v-text-field
                v-model="searchQuery"
                :label="$t('projects.search', 'Search projects')"
                prepend-inner-icon="mdi-magnify"
                clearable
                hide-details
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-select
                v-model="selectedContinent"
                :items="continentOptions"
                :label="$t('projects.filterByContinent', 'Filter by continent')"
                clearable
                hide-details
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6" md="4">
              <v-autocomplete
                v-model="selectedCountries"
                :items="countryOptions"
                :label="$t('projects.filterByCountry', 'Filter by country')"
                multiple
                chips
                closable-chips
                clearable
                hide-details
                density="comfortable"
              />
            </v-col>
            
            <!-- Row 2 -->
            <v-col cols="12" sm="6" md="3">
              <v-select
                v-model="selectedStatus"
                :items="statusOptions"
                :label="$t('projects.filterByStatus', 'Filter by status')"
                clearable
                hide-details
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-autocomplete
                v-model="selectedThematics"
                :items="thematicOptions"
                :label="$t('projects.filterByThematic', 'Filter by thematics')"
                multiple
                chips
                closable-chips
                clearable
                hide-details
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-autocomplete
                v-model="selectedFields"
                :items="fieldOptions"
                :label="$t('projects.filterByField', 'Filter by fields')"
                multiple
                chips
                closable-chips
                clearable
                hide-details
                density="comfortable"
              />
            </v-col>
            <v-col cols="12" sm="6" md="3">
              <v-autocomplete
                v-model="selectedTypes"
                :items="typeOptions"
                :label="$t('projects.filterByType', 'Filter by types')"
                multiple
                chips
                closable-chips
                clearable
                hide-details
                density="comfortable"
              />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Results count -->
      <div class="text-center mb-4">
        <p class="text-body-1">
          {{ filteredProjects.length }} {{ $t('projects.projectsFound', 'projects found') }}
        </p>
      </div>

      <!-- Project list -->
      <v-row v-if="filteredProjects.length > 0">
        <v-col v-for="project in paginatedProjects" :key="project.pubId" cols="12" md="6" lg="4">
          <v-card class="h-100" hover style="cursor: pointer" @click="handleProjectClick(project)">
            <v-card-title class="text-h6">
              {{ project.name }}
            </v-card-title>
            <v-card-subtitle>
              <v-chip
                v-if="project.status !== undefined"
                size="small"
                class="mr-2"
                :color="getStatusColor(project.status)"
              >
                {{ getStatusLabel(project.status) }}
              </v-chip>
              <span v-if="project.location">{{ project.location }}</span>
            </v-card-subtitle>
            <v-card-text>
              <p class="text-body-2 line-clamp-3">
                {{ project.description }}
              </p>
              <div class="mt-4">
                <v-chip
                  v-for="continentId in project.continent || []"
                  :key="continentId"
                  size="x-small"
                  class="mr-1 mb-1"
                >
                  {{ getContinentLabel(continentId) }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>
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
const { t: $t, locale } = useI18n()
const route = useRoute()
const router = useRouter()
const { getStatusLabel, getContinentLabel, getCountryLabel } = useProjectMappings()

// Fetch all projects from the collection
const { data: projectsData, error } = await useAsyncData('projects', async () => {
  try {
    const result = await queryCollection('projects').all()
    console.log('Query result:', {
      type: typeof result,
      isArray: Array.isArray(result),
      length: Array.isArray(result) ? result.length : 'N/A',
      sample: result?.[0] ? Object.keys(result[0]) : 'No sample'
    })
    return result
  } catch (e) {
    console.error('Query error:', e)
    throw e
  }
})

// Debug logging
if (error.value) {
  console.error('Error loading projects:', error.value)
}

const projects = computed(() => {
  if (!projectsData.value) {
    console.warn('No projects data available - projectsData.value is:', projectsData.value)
    return []
  }

  // Nuxt Content returns data collections as an array directly
  const data = Array.isArray(projectsData.value) ? projectsData.value : []
  console.log(`Loaded ${data.length} projects`)
  if (data.length > 0) {
    console.log('First project stem:', data[0].stem)
    console.log('First project pubId:', data[0].pubId)
  }
  return data
})

// Filter state
const searchQuery = ref('')
const selectedContinent = ref<string | null>(null)
const selectedCountries = ref<string[]>([])
const selectedStatus = ref<string | null>(null)
const selectedThematics = ref<string[]>([])
const selectedFields = ref<string[]>([])
const selectedTypes = ref<string[]>([])
const currentPage = ref(1)
const itemsPerPage = 12

// Initialize filters from URL query
onMounted(() => {
  if (route.query.countries) {
    const countriesParam = route.query.countries
    selectedCountries.value = Array.isArray(countriesParam)
      ? countriesParam
      : [countriesParam as string]
  }
  if (route.query.continent) {
    selectedContinent.value = route.query.continent as string
  }
  if (route.query.status) {
    selectedStatus.value = route.query.status as string
  }
  if (route.query.thematics) {
    const thematicsParam = route.query.thematics
    selectedThematics.value = Array.isArray(thematicsParam)
      ? thematicsParam
      : [thematicsParam as string]
  }
  if (route.query.fields) {
    const fieldsParam = route.query.fields
    selectedFields.value = Array.isArray(fieldsParam) ? fieldsParam : [fieldsParam as string]
  }
  if (route.query.types) {
    const typesParam = route.query.types
    selectedTypes.value = Array.isArray(typesParam) ? typesParam : [typesParam as string]
  }
})

// Update URL when filters change
watch(
  [selectedCountries, selectedContinent, selectedStatus, selectedThematics, selectedFields, selectedTypes],
  () => {
    const query: Record<string, string | string[]> = {}
    if (selectedCountries.value.length > 0) {
      query.countries = selectedCountries.value
    }
    if (selectedContinent.value) {
      query.continent = selectedContinent.value
    }
    if (selectedStatus.value) {
      query.status = selectedStatus.value
    }
    if (selectedThematics.value.length > 0) {
      query.thematics = selectedThematics.value
    }
    if (selectedFields.value.length > 0) {
      query.fields = selectedFields.value
    }
    if (selectedTypes.value.length > 0) {
      query.types = selectedTypes.value
    }
    router.push({ query })
  }
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

// Thematics options for filter - get unique thematics from all projects
const { getThematicLabel, getFieldLabel, getTypeLabel } = useProjectMappings()

const thematicOptions = computed(() => {
  const thematics = new Set<string>()
  projects.value.forEach((project) => {
    if (project.thematic && Array.isArray(project.thematic)) {
      project.thematic.forEach((t: string) => thematics.add(t))
    }
  })
  return Array.from(thematics)
    .sort()
    .map((code) => ({
      value: code,
      title: getThematicLabel(code)
    }))
})

// Fields options for filter - get unique fields from all projects
const fieldOptions = computed(() => {
  const fields = new Set<string>()
  projects.value.forEach((project) => {
    if (project.field && Array.isArray(project.field)) {
      project.field.forEach((f: string) => fields.add(f))
    }
  })
  return Array.from(fields)
    .sort()
    .map((code) => ({
      value: code,
      title: getFieldLabel(code)
    }))
})

// Types options for filter - get unique types from all projects
const typeOptions = computed(() => {
  const types = new Set<string>()
  projects.value.forEach((project) => {
    if (project.type && Array.isArray(project.type)) {
      project.type.forEach((t: string) => types.add(t))
    }
  })
  return Array.from(types)
    .sort()
    .map((code) => ({
      value: code,
      title: getTypeLabel(code)
    }))
})

// Filtered projects
const filteredProjects = computed(() => {
  let filtered = projects.value.filter((p) => !p.removedAt)

  // Search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(
      (p) =>
        p.name?.toLowerCase().includes(query) ||
        p.description?.toLowerCase().includes(query) ||
        p.location?.toLowerCase().includes(query)
    )
  }

  // Continent filter
  if (selectedContinent.value !== null) {
    filtered = filtered.filter((p) => p.continent?.includes(selectedContinent.value as string))
  }

  // Country filter
  if (selectedCountries.value.length > 0) {
    filtered = filtered.filter((p) =>
      p.country?.some((c: string) => selectedCountries.value.includes(c))
    )
  }

  // Status filter
  if (selectedStatus.value !== null) {
    filtered = filtered.filter((p) => p.status === selectedStatus.value)
  }

  // Thematics filter
  if (selectedThematics.value.length > 0) {
    filtered = filtered.filter((p) =>
      p.thematic?.some((t: string) => selectedThematics.value.includes(t))
    )
  }

  // Fields filter
  if (selectedFields.value.length > 0) {
    filtered = filtered.filter((p) =>
      p.field?.some((f: string) => selectedFields.value.includes(f))
    )
  }

  // Types filter
  if (selectedTypes.value.length > 0) {
    filtered = filtered.filter((p) => p.type?.some((t: string) => selectedTypes.value.includes(t)))
  }

  // Sort by score (descending)
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
  [
    searchQuery,
    selectedContinent,
    selectedCountries,
    selectedStatus,
    selectedThematics,
    selectedFields,
    selectedTypes
  ],
  () => {
    currentPage.value = 1
  }
)

// Navigation handler
const handleProjectClick = async (project: any) => {
  const projectId = project.stem.replace('projects/', '')
  const targetPath = `/projects/${projectId}`
  console.log('=== NAVIGATION ATTEMPT ===')
  console.log('Project:', project.name)
  console.log('Project stem:', project.stem)
  console.log('Project pubId:', project.pubId)
  console.log('Target path:', targetPath)
  try {
    await navigateTo(targetPath)
    console.log('Navigation successful')
  } catch (error) {
    console.error('Navigation error:', error)
  }
}

// Status color helper
const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending':
      return 'grey'
    case 'published':
      return 'blue'
    case 'stale':
      return 'orange'
    case 'verified':
      return 'green'
    case 'new':
      return 'purple'
    default:
      return 'grey'
  }
}

useHead({
  title: $t('nav.projects')
})
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
