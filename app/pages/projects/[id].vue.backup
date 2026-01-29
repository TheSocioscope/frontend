<template>
  <div>
    <!-- Loading state -->
    <v-container v-if="!project && !projectError" class="py-16">
      <div class="text-center">
        <v-progress-circular indeterminate color="primary" size="64" />
        <p class="text-h6 mt-4">{{ $t('projects.loading', 'Loading project...') }}</p>
      </div>
    </v-container>

    <v-container v-else-if="project" class="py-16">
      <!-- Breadcrumbs -->
      <v-breadcrumbs :items="breadcrumbs" class="px-0" />

      <!-- Translation Disclaimer -->
      <TranslationDisclaimer
        v-if="(project as any).originalLang && showDisclaimer"
        :original-lang="(project as any).originalLang"
        :current-locale="currentLocale"
        :showing-original="showOriginal"
        @toggle-original="toggleOriginal"
      />

      <!-- Project header -->
      <div class="mb-8">
        <v-chip
          v-if="project.status !== undefined"
          :color="getStatusColor(String(project.status))"
          class="mb-4"
        >
          {{ getStatusLabel(String(project.status)) }}
        </v-chip>
        <h1 class="text-h3 mb-4">{{ localizedName }}</h1>

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
          <!-- YouTube Video Embed -->
          <v-card v-if="project.yt" class="mb-6 video-card" elevation="4">
            <div class="video-container">
              <iframe
                :src="getYouTubeEmbedUrl(project.yt)"
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen
                class="youtube-embed"
              />
            </div>
          </v-card>

          <!-- Description -->
          <v-card class="mb-4">
            <v-card-title>{{ $t('projects.description', 'Description') }}</v-card-title>
            <v-card-text>
              <p class="text-body-1">{{ localizedDescription }}</p>
            </v-card-text>
          </v-card>

          <!-- Website Link -->
          <v-card v-if="project.url" class="mb-4">
            <v-card-title>{{ $t('projects.links', 'Links') }}</v-card-title>
            <v-card-text>
              <v-btn
                :href="project.url"
                target="_blank"
                variant="outlined"
                prepend-icon="mdi-open-in-new"
                class="mr-2 mb-2"
              >
                {{ $t('projects.website', 'Website') }}
              </v-btn>
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
                <p class="text-subtitle-2 mb-2">
                  {{ $t('projects.continentsLabel', 'Continents') }}
                </p>
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
                <p class="text-subtitle-2 mb-2">{{ $t('projects.countriesLabel', 'Countries') }}</p>
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
            <v-card-title>{{ $t('labels.fields', 'Fields') }}</v-card-title>
            <v-card-text>
              <v-chip
                v-for="fieldId in project.field"
                :key="fieldId"
                size="small"
                color="blue-darken-2"
                class="mr-1 mb-1"
              >
                {{ getFieldLabel(fieldId) }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Thematics -->
          <v-card v-if="project.thematic?.length" class="mb-4">
            <v-card-title>{{ $t('labels.thematics', 'Thematics') }}</v-card-title>
            <v-card-text>
              <v-chip
                v-for="thematicId in project.thematic"
                :key="thematicId"
                size="small"
                color="green-darken-2"
                class="mr-1 mb-1"
              >
                {{ getThematicLabel(thematicId) }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Types -->
          <v-card v-if="project.type?.length" class="mb-4">
            <v-card-title>{{ $t('labels.types', 'Types') }}</v-card-title>
            <v-card-text>
              <v-chip
                v-for="typeId in project.type"
                :key="typeId"
                size="small"
                color="purple-darken-2"
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
              <v-chip color="orange-darken-2">
                {{ getStateLabel(project.state) }}
              </v-chip>
            </v-card-text>
          </v-card>

          <!-- Periodicity -->
          <v-card v-if="(project as any).periodicity" class="mb-4">
            <v-card-title>{{ $t('projects.periodicity', 'Periodicity') }}</v-card-title>
            <v-card-text>
              <v-chip>
                {{ getPeriodicityLabel((project as any).periodicity) }}
              </v-chip>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Back button -->
      <div class="text-center mt-8">
        <v-btn :to="localePath('/projects')" prepend-icon="mdi-arrow-left" variant="outlined">
          {{ $t('projects.backToList', 'Back to projects') }}
        </v-btn>
      </div>
    </v-container>

    <!-- Not found -->
    <v-container v-else class="py-16">
      <v-card class="text-center pa-8">
        <v-icon size="64" color="grey-lighten-1">mdi-file-document-remove-outline</v-icon>
        <p class="text-h5 mt-4">{{ $t('projects.notFound', 'Project not found') }}</p>
        <v-btn :to="localePath('/projects')" class="mt-4" color="primary">
          {{ $t('projects.backToList', 'Back to projects') }}
        </v-btn>
      </v-card>
    </v-container>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { t: $t, locale } = useI18n()
const localePath = useLocalePath()
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
const { isTranslated: checkIsTranslated } = useMultilingual()

// State for toggling between current locale and original language
const showOriginal = ref(false)

const projectId = computed(() => route.params.id as string)

// First, let's try fetching all projects to see what stems actually exist
const { data: project, error: projectError } = await useAsyncData(
  `project-${projectId.value}`,
  async () => {
    try {
      // Get all projects to debug
      const allProjects = await queryCollection('projects').all()
      console.log('Total projects in collection:', allProjects.length)
      console.log('Looking for project with ID:', projectId.value)

      // Try to find by pubId instead of stem
      const foundByPubId = allProjects.find((p) => String(p.pubId) === String(projectId.value))

      if (foundByPubId) {
        console.log('Found project by pubId:', foundByPubId.name)
        console.log('Project stem:', foundByPubId.stem)
        return foundByPubId
      }

      // Try by stem as fallback
      const stemPath = `projects/${projectId.value}`
      const foundByStem = allProjects.find((p) => p.stem === stemPath)

      if (foundByStem) {
        console.log('Found project by stem:', foundByStem.name)
        return foundByStem
      }

      console.error('Project not found with pubId or stem:', projectId.value)
      console.log(
        'Sample stems from collection:',
        allProjects.slice(0, 3).map((p) => ({ pubId: p.pubId, stem: p.stem }))
      )
      return null
    } catch (e) {
      console.error('Error loading project:', e)
      return null
    }
  }
)

// Breadcrumbs
const breadcrumbs = computed(() => [
  {
    title: $t('nav.projects'),
    to: '/projects'
  },
  {
    title: localizedName.value || projectId.value,
    disabled: true
  }
])

// Format date helper
const formatDate = (timestamp: number) => {
  return new Date(timestamp * 1000).toLocaleDateString()
}

// Status color helper
const getStatusColor = (status: string) => {
  // Only verified (status 3) is green, all others are gray
  return status === '3' || status === 'verified' ? 'green' : 'grey'
}

// Extract YouTube video ID from various URL formats or return if already an ID
const getYouTubeEmbedUrl = (urlOrId: string) => {
  // If it's already just a video ID (no URL format), use it directly
  if (!urlOrId.includes('/') && !urlOrId.includes('http')) {
    return `https://www.youtube.com/embed/${urlOrId}`
  }

  // Otherwise parse as URL
  try {
    const urlObj = new URL(urlOrId)
    let videoId = ''

    // Handle different YouTube URL formats
    if (urlObj.hostname.includes('youtube.com')) {
      videoId = urlObj.searchParams.get('v') || ''
    } else if (urlObj.hostname.includes('youtu.be')) {
      videoId = urlObj.pathname.slice(1)
    }

    return `https://www.youtube.com/embed/${videoId}`
  } catch {
    // If URL parsing fails, assume it's a video ID
    return `https://www.youtube.com/embed/${urlOrId}`
  }
}

// Computed properties for multilingual content
const currentLocale = computed(() => {
  const proj = project.value as any
  return showOriginal.value ? proj?.originalLang || 'en' : locale.value
})

const localizedName = computed(() => {
  const proj = project.value as any
  if (!proj?.name) return ''
  const textObj = proj.name
  if (typeof textObj === 'string') return textObj

  const targetLocale = showOriginal.value ? proj.originalLang || 'en' : locale.value
  const origLang = proj.originalLang || 'en'
  return (
    (textObj as Record<string, string>)[targetLocale] ||
    (textObj as Record<string, string>)[origLang] ||
    (textObj as Record<string, string>).en ||
    ''
  )
})

const localizedDescription = computed(() => {
  const proj = project.value as any
  if (!proj?.description) return ''
  const textObj = proj.description
  if (typeof textObj === 'string') return textObj

  const targetLocale = showOriginal.value ? proj.originalLang || 'en' : locale.value
  const origLang = proj.originalLang || 'en'
  return (
    (textObj as Record<string, string>)[targetLocale] ||
    (textObj as Record<string, string>)[origLang] ||
    (textObj as Record<string, string>).en ||
    ''
  )
})

const isTranslated = computed(() => {
  const proj = project.value as any
  return !showOriginal.value && checkIsTranslated(proj?.originalLang)
})

const showDisclaimer = computed(() => {
  const proj = project.value as any
  // Show disclaimer if original language exists and is different from current locale
  return proj?.originalLang && proj.originalLang !== locale.value
})

// Toggle between original and translated version
const toggleOriginal = () => {
  showOriginal.value = !showOriginal.value
}

// SEO - use watchEffect to update dynamically
watchEffect(() => {
  useHead({
    title: localizedName.value || $t('nav.projects'),
    meta: [
      {
        name: 'description',
        content: localizedDescription.value || ''
      }
    ]
  })
})
</script>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}

.video-card {
  overflow: hidden;
  background: #000;
}

.video-container {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
}

.youtube-embed {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}
</style>
