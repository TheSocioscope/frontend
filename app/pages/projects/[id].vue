<template>
  <div class="project-detail">
    <!-- Loading state -->
    <div v-if="!project && !projectError" class="loading-container">
      <v-progress-circular indeterminate color="primary" size="64" />
      <p>{{ $t('common.loading') }}</p>
    </div>

    <!-- Error state -->
    <div v-else-if="projectError" class="not-found-container">
      <div class="not-found-content">
        <v-icon size="80" color="error">mdi-alert-circle</v-icon>
        <h1>{{ $t('common.notFound') }}</h1>
        <p>{{ $t('common.projectNotFoundDescription') }}</p>
        <v-btn :to="localePath('/projects')" color="primary" size="large">
          {{ $t('common.browseProjects') }}
        </v-btn>
      </div>
    </div>

    <!-- Project content -->
    <div v-else-if="project" class="project-container">
      <!-- Header Component -->
      <ProjectHeader
        :project="project"
        :localized-name="localizedName"
        :show-original="showOriginal"
        :show-disclaimer="showDisclaimer"
      />

      <v-container class="content-container">
        <!-- Translation Disclaimer -->
        <ProjectTranslationDisclaimer
          v-if="showDisclaimer"
          :original-lang="project.originalLang"
          :current-locale="String(locale)"
          :showing-original="showOriginal"
          @toggle-language="toggleOriginal"
        />

        <!-- About Component -->
        <ProjectAbout :project="project" :localized-description="localizedDescription" />

        <!-- Video Component -->
        <ProjectVideo v-if="project.yt" :project="project" />

        <!-- Timeline Component -->
        <ProjectTimeline
          v-if="localizedTimeline && localizedTimeline.length > 0"
          :localized-timeline="localizedTimeline"
        />

        <!-- Offers Component -->
        <ProjectOffers
          v-if="localizedOffers && localizedOffers.length > 0"
          :localized-offers="localizedOffers"
        />

        <!-- Looking For Component -->
        <ProjectLookingFor
          v-if="localizedLookingFor && localizedLookingFor.length > 0"
          :localized-looking-for="localizedLookingFor"
        />

        <!-- Team Component -->
        <ProjectTeam v-if="project.team && project.team.length > 0" :project="project" />

        <!-- Gallery Component -->
        <ProjectGallery
          v-if="localizedGallery && localizedGallery.length > 0"
          :localized-gallery="localizedGallery"
        />

        <!-- Share Component -->
        <ProjectShare :project-name="localizedName" :project-url="currentUrl" />
      </v-container>

      <!-- Floating Action Button -->
      <v-btn
        :to="localePath('/projects')"
        class="floating-back-btn"
        color="primary"
        icon
        size="large"
        elevation="8"
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
    </div>
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
  getPeriodicityLabel
} = useProjectMappings()
const { isTranslated: checkIsTranslated } = useMultilingual()

// State for toggling between current locale and original language
const showOriginal = ref(false)

const projectId = computed(() => route.params.id as string)

// Current URL for sharing
const currentUrl = computed(() => {
  if (import.meta.client) {
    return window.location.href
  }
  return ''
})

// Fetch project
const { data: project, error: projectError } = await useAsyncData(
  `project-${projectId.value}`,
  async () => {
    try {
      const projects = await queryCollection('projects').all()
      const foundProject = projects.find(
        (p: any) => String(p.pubId) === projectId.value || p._path?.includes(projectId.value)
      )

      if (!foundProject) {
        throw new Error('Project not found')
      }

      return foundProject
    } catch (e) {
      console.error('Error loading project:', e)
      return null
    }
  }
)

// Computed properties for multilingual content
const currentLocale = computed(() => {
  const proj = project.value as any
  return showOriginal.value ? proj?.originalLang || 'en' : locale.value
})

const localizedName = computed(() => {
  const proj = project.value as any
  if (!proj) return ''
  if (typeof proj.name === 'string') return proj.name
  return proj.name?.[currentLocale.value] || proj.name?.en || proj.name || ''
})

const localizedDescription = computed(() => {
  const proj = project.value as any
  if (!proj) return ''
  if (typeof proj.description === 'string') return proj.description
  return proj.description?.[currentLocale.value] || proj.description?.en || proj.description || ''
})

const localizedTimeline = computed(() => {
  const proj = project.value as any
  if (!proj) return []

  // Check both direct access and meta object
  const timelineData = proj.timeline || proj.meta?.timeline
  if (!timelineData) return []

  return timelineData.map((item: any) => ({
    date: item.date || '',
    icon: item.icon || '',
    text:
      typeof item.text === 'string'
        ? item.text
        : item.text?.[currentLocale.value] || item.text?.en || ''
  }))
})

const localizedOffers = computed(() => {
  const proj = project.value as any
  if (!proj) return []

  // Check both direct access and meta object
  const offersData = proj.offers || proj.meta?.offers
  if (!offersData) return []

  return offersData.map((item: any) => ({
    title:
      typeof item.label === 'string'
        ? item.label
        : item.label?.[currentLocale.value] || item.label?.en || '',
    description:
      typeof item.description === 'string'
        ? item.description
        : item.description?.[currentLocale.value] || item.description?.en || '',
    image: item.image || '',
    url: item.url || '',
    icon: item.icon || ''
  }))
})

const localizedLookingFor = computed(() => {
  const proj = project.value as any
  if (!proj) return []

  // Check both direct access and meta object
  const lookingForData = proj.lookingFor || proj.meta?.lookingFor
  if (!lookingForData) return []

  return lookingForData.map((item: any) => ({
    title:
      typeof item.label === 'string'
        ? item.label
        : item.label?.[currentLocale.value] || item.label?.en || '',
    description:
      typeof item.description === 'string'
        ? item.description
        : item.description?.[currentLocale.value] || item.description?.en || '',
    icon: item.icon || ''
  }))
})

const localizedGallery = computed(() => {
  const proj = project.value as any
  if (!proj) return []

  // Check both direct access and meta object
  const galleryData = proj.gallery || proj.meta?.gallery
  if (!galleryData) return []

  return galleryData.map((item: any) => ({
    url: item.url || '',
    caption:
      typeof item.caption === 'string'
        ? item.caption
        : item.caption?.[currentLocale.value] || item.caption?.en || ''
  }))
})

const showDisclaimer = computed(() => {
  const proj = project.value as any
  return proj?.originalLang && proj.originalLang !== locale.value
})

// Toggle between original and translated version
const toggleOriginal = () => {
  showOriginal.value = !showOriginal.value
}

// Debug logging
if (import.meta.client) {
  watch(
    [project, localizedTimeline, localizedOffers, localizedLookingFor, localizedGallery],
    () => {
      console.log('=== Project Data Debug ===')
      console.log('Project:', project.value)
      console.log('Timeline:', localizedTimeline.value, 'Length:', localizedTimeline.value?.length)
      console.log('Offers:', localizedOffers.value, 'Length:', localizedOffers.value?.length)
      console.log(
        'LookingFor:',
        localizedLookingFor.value,
        'Length:',
        localizedLookingFor.value?.length
      )
      console.log('Gallery:', localizedGallery.value, 'Length:', localizedGallery.value?.length)
    },
    { immediate: true }
  )
}

// SEO
watchEffect(() => {
  if (project.value) {
    useHead({
      title: localizedName.value,
      meta: [
        { name: 'description', content: localizedDescription.value },
        { property: 'og:title', content: localizedName.value },
        { property: 'og:description', content: localizedDescription.value },
        { property: 'og:type', content: 'website' },
        { property: 'og:url', content: currentUrl.value }
      ]
    })
  }
})
</script>

<style scoped lang="scss">
.project-detail {
  min-height: 100vh;
  background: #f8f9fa;
}

.loading-container,
.not-found-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 1.5rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;
  padding: 2rem;

  h1 {
    font-size: 2rem;
    font-weight: 700;
    margin: 1rem 0;
  }

  p {
    font-size: 1.125rem;
    margin-bottom: 2rem;
  }
}

.project-container {
  position: relative;
}

.content-container {
  max-width: 1400px;
  padding: 2rem 1rem;
}

.floating-back-btn {
  position: fixed;
  bottom: 2rem;
  left: 2rem;
  z-index: 100;
}

@media (max-width: 768px) {
  .content-container {
    padding: 1rem 0.5rem;
  }

  .floating-back-btn {
    bottom: 1rem;
    left: 1rem;
  }
}
</style>
