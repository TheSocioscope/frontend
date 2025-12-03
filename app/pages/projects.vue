<template>
  <div>
    <v-container class="py-16">
      <h1 class="text-h2 text-center mb-8">{{ $t('nav.projects') }}</h1>

      <!-- Filters -->
      <v-card class="mb-8">
        <v-card-text>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="searchQuery"
                :label="$t('projects.search', 'Search projects')"
                prepend-inner-icon="mdi-magnify"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="selectedContinent"
                :items="continentOptions"
                :label="$t('projects.filterByContinent', 'Filter by continent')"
                clearable
                hide-details
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="selectedStatus"
                :items="statusOptions"
                :label="$t('projects.filterByStatus', 'Filter by status')"
                clearable
                hide-details
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
          <v-card :to="`/projects/${project.pubId}`" class="h-100" hover>
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
const { getStatusLabel, getContinentLabel } = useProjectMappings()

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
  return data
})

// Filter state
const searchQuery = ref('')
const selectedContinent = ref<number | null>(null)
const selectedStatus = ref<number | null>(null)
const currentPage = ref(1)
const itemsPerPage = 12

// Continent options for filter
const continentOptions = computed(() => {
  const options = []
  for (let i = 0; i <= 7; i++) {
    options.push({
      value: i,
      title: getContinentLabel(i)
    })
  }
  return options
})

// Status options for filter
const statusOptions = computed(() => {
  return [
    { value: 0, title: getStatusLabel(0) },
    { value: 1, title: getStatusLabel(1) },
    { value: 2, title: getStatusLabel(2) },
    { value: 3, title: getStatusLabel(3) },
    { value: 7, title: getStatusLabel(7) }
  ]
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
    filtered = filtered.filter((p) => p.continent?.includes(selectedContinent.value as number))
  }

  // Status filter
  if (selectedStatus.value !== null) {
    filtered = filtered.filter((p) => p.status === selectedStatus.value)
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
watch([searchQuery, selectedContinent, selectedStatus], () => {
  currentPage.value = 1
})

// Status color helper
const getStatusColor = (status: number) => {
  switch (status) {
    case 0:
      return 'grey'
    case 1:
      return 'blue'
    case 2:
      return 'orange'
    case 3:
      return 'green'
    case 7:
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
