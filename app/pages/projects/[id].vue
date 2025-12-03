<template>
  <div>
    <v-container v-if="project" class="py-16">
      <!-- Breadcrumbs -->
      <v-breadcrumbs :items="breadcrumbs" class="px-0" />

      <!-- Project header -->
      <div class="mb-8">
        <v-chip
          v-if="project.status !== undefined"
          :color="getStatusColor(project.status)"
          class="mb-4"
        >
          {{ getStatusLabel(project.status) }}
        </v-chip>
        <h1 class="text-h3 mb-4">{{ project.name }}</h1>

        <!-- Project metadata -->
        <div class="d-flex flex-wrap gap-2 mb-4">
          <v-chip v-if="project.location" prepend-icon="mdi-map-marker">
            {{ project.location }}
          </v-chip>
          <v-chip v-if="project.lang" prepend-icon="mdi-translate">
            {{ project.lang.toUpperCase() }}
          </v-chip>
          <v-chip v-if="project.createdAt" prepend-icon="mdi-calendar">
            {{ formatDate(project.createdAt) }}
          </v-chip>
          <v-chip v-if="project.score" prepend-icon="mdi-star">
            {{ $t('projects.score', 'Score') }}: {{ Math.round(project.score) }}
          </v-chip>
        </div>
      </div>

      <v-row>
        <!-- Main content -->
        <v-col cols="12" md="8">
          <!-- Description -->
          <v-card class="mb-4">
            <v-card-title>{{ $t('projects.description', 'Description') }}</v-card-title>
            <v-card-text>
              <p class="text-body-1">{{ project.description }}</p>
            </v-card-text>
          </v-card>

          <!-- Links -->
          <v-card v-if="project.url || project.yt" class="mb-4">
            <v-card-title>{{ $t('projects.links', 'Links') }}</v-card-title>
            <v-card-text>
              <v-btn
                v-if="project.url"
                :href="project.url"
                target="_blank"
                variant="outlined"
                prepend-icon="mdi-open-in-new"
                class="mr-2 mb-2"
              >
                {{ $t('projects.website', 'Website') }}
              </v-btn>
              <v-btn
                v-if="project.yt"
                :href="project.yt"
                target="_blank"
                variant="outlined"
                prepend-icon="mdi-youtube"
                color="red"
                class="mb-2"
              >
                {{ $t('projects.video', 'Video') }}
              </v-btn>
            </v-card-text>
          </v-card>

          <!-- Contact -->
          <v-card v-if="project.contact" class="mb-4">
            <v-card-title>{{ $t('projects.contact', 'Contact') }}</v-card-title>
            <v-card-text>
              <p class="text-body-1">
                <v-icon class="mr-2">mdi-account</v-icon>
                {{ project.contact.firstname }} {{ project.contact.lastname }}
              </p>
            </v-card-text>
          </v-card>
        </v-col>

        <!-- Sidebar -->
        <v-col cols="12" md="4">
          <!-- Geographic info -->
          <v-card v-if="project.continent?.length || project.country?.length" class="mb-4">
            <v-card-title>{{ $t('projects.geography', 'Geography') }}</v-card-title>
            <v-card-text>
              <div v-if="project.continent?.length" class="mb-3">
                <p class="text-subtitle-2 mb-2">{{ $t('projects.continents', 'Continents') }}</p>
                <v-chip
                  v-for="continentId in project.continent"
                  :key="continentId"
                  size="small"
                  class="mr-1 mb-1"
                >
                  {{ getContinentLabel(continentId) }}
                </v-chip>
              </div>
              <div v-if="project.country?.length">
                <p class="text-subtitle-2 mb-2">{{ $t('projects.countries', 'Countries') }}</p>
                <v-chip
                  v-for="countryId in project.country"
                  :key="countryId"
                  size="small"
                  class="mr-1 mb-1"
                >
                  {{ getCountryLabel(countryId) }}
                </v-chip>
              </div>
            </v-card-text>
          </v-card>

          <!-- Fields -->
          <v-card v-if="project.field?.length" class="mb-4">
            <v-card-title>{{ $t('projects.fields', 'Fields') }}</v-card-title>
            <v-card-text>
              <v-chip
                v-for="fieldId in project.field"
                :key="fieldId"
                size="small"
                color="blue-lighten-4"
                class="mr-1 mb-1"
              >
                {{ getFieldLabel(fieldId) }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Thematics -->
          <v-card v-if="project.thematic?.length" class="mb-4">
            <v-card-title>{{ $t('projects.thematics', 'Thematics') }}</v-card-title>
            <v-card-text>
              <v-chip
                v-for="thematicId in project.thematic"
                :key="thematicId"
                size="small"
                color="green-lighten-4"
                class="mr-1 mb-1"
              >
                {{ getThematicLabel(thematicId) }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Types -->
          <v-card v-if="project.type?.length" class="mb-4">
            <v-card-title>{{ $t('projects.types', 'Types') }}</v-card-title>
            <v-card-text>
              <v-chip
                v-for="typeId in project.type"
                :key="typeId"
                size="small"
                color="purple-lighten-4"
                class="mr-1 mb-1"
              >
                {{ getTypeLabel(typeId) }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- State -->
          <v-card v-if="project.state !== undefined" class="mb-4">
            <v-card-title>{{ $t('projects.projectState', 'Project State') }}</v-card-title>
            <v-card-text>
              <v-chip color="orange-lighten-4">
                {{ getStateLabel(project.state) }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Periodicity -->
          <v-card v-if="project.periodicity" class="mb-4">
            <v-card-title>{{ $t('projects.periodicity', 'Periodicity') }}</v-card-title>
            <v-card-text>
              <v-chip>
                {{ getPeriodicityLabel(project.periodicity) }}
              </v-chip>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Back button -->
      <div class="text-center mt-8">
        <v-btn to="/projects" prepend-icon="mdi-arrow-left" variant="outlined">
          {{ $t('projects.backToList', 'Back to projects') }}
        </v-btn>
      </div>
    </v-container>

    <!-- Not found -->
    <v-container v-else class="py-16">
      <v-card class="text-center pa-8">
        <v-icon size="64" color="grey-lighten-1">mdi-file-document-remove-outline</v-icon>
        <p class="text-h5 mt-4">{{ $t('projects.notFound', 'Project not found') }}</p>
        <v-btn to="/projects" class="mt-4" color="primary">
          {{ $t('projects.backToList', 'Back to projects') }}
        </v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { t: $t } = useI18n()
const {
  getStatusLabel,
  getContinentLabel,
  getCountryLabel,
  getFieldLabel,
  getThematicLabel,
  getTypeLabel,
  getStateLabel,
  getPeriodicityLabel
} = useProjectMappings()

const projectId = computed(() => route.params.id as string)

// Fetch the specific project by its pubId
const { data: project, error } = await useAsyncData(`project-${projectId.value}`, async () => {
  try {
    const result = await queryCollection('projects')
      .where('pubId', '=', Number(projectId.value))
      .first()
    if (import.meta.client) {
      console.log('Project loaded:', result?.name || 'Not found')
    }
    return result
  } catch (e) {
    if (import.meta.client) {
      console.error('Error loading project:', e)
    }
    return null
  }
})

// Handle not found
if (!project.value) {
  throw createError({
    statusCode: 404,
    statusMessage: 'Project not found',
    fatal: true
  })
}

// Breadcrumbs
const breadcrumbs = computed(() => [
  {
    title: $t('nav.projects'),
    to: '/projects'
  },
  {
    title: project.value?.name || projectId.value,
    disabled: true
  }
])

// Format date helper
const formatDate = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleDateString()
}

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

// SEO
useHead({
  title: project.value?.name || $t('nav.projects')
})
</script>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}
</style>
