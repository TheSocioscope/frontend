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
      <!-- Breadcrumb (Phase 2) -->
      <ProjectBreadcrumb
        v-if="detailV2"
        :localized-name="localizedName"
        :page-url="currentUrl"
        @edit="editDrawerOpen = true"
      />

      <div class="detail-grid">
        <main class="detail-main">
          <!-- Header card — title + location + the entire "About" body
               (entity-summary + description) live inside this card.
               No separate ProjectAbout section beneath. -->
          <ProjectHeader
            :project="project"
            :localized-name="localizedName"
            :localized-description="localizedDescription"
            :show-original="showOriginal"
            :show-disclaimer="showDisclaimer"
          />

          <!-- Primary action bar — placed AFTER About so the user reads
               the project description first, then chooses to Connect /
               visit Website. -->
          <div class="action-bar" v-if="detailV2">
            <v-btn
              class="action-connect"
              color="success"
              variant="flat"
              prepend-icon="mdi-account-plus-outline"
              size="default"
              density="comfortable"
              @click="connectDrawerOpen = true"
            >
              {{ $t('projects.detail.connect', 'Connect') }}
            </v-btn>
            <v-btn
              v-if="project.url"
              class="action-website"
              :href="project.url"
              target="_blank"
              rel="noopener noreferrer"
              color="primary"
              variant="outlined"
              append-icon="mdi-open-in-new"
              size="default"
              density="comfortable"
            >
              {{ $t('projects.detail.website', 'Website') }}
            </v-btn>
          </div>

          <!-- Video Component -->
          <ProjectVideo v-if="project.yt" :project="project" />

          <!-- Team Component -->
          <ProjectTeam v-if="project.team && project.team.length > 0" :project="project" />

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

          <!-- Share Component (mobile fallback; hidden on desktop where sidebar carries it) -->
          <ProjectShare class="share-mobile-fallback" :project-name="localizedName" :project-url="currentUrl" />
        </main>

        <!-- Meta sidebar + similar initiatives — right column on desktop,
             below content on tablet/mobile. Wrapped together so they
             stay in the same grid track. -->
        <div class="detail-sidebar-column">
          <ProjectMetaSidebar
            v-if="detailV2"
            :project="project"
            :localized-name="localizedName"
            :page-url="currentUrl"
            class="detail-sidebar"
            @connect="connectDrawerOpen = true"
            @edit="editDrawerOpen = true"
          />

          <ProjectRelated :current-project="project" />
        </div>
      </div>

      <!-- Connect Drawer -->
      <ProjectConnectDrawer
        :is-open="connectDrawerOpen"
        :project="project"
        :localized-name="localizedName"
        :page-url="currentUrl"
        @close="connectDrawerOpen = false"
      />

      <!-- Edit Drawer -->
      <ProjectEditDrawer
        :is-open="editDrawerOpen"
        :project="project"
        :localized-name="localizedName"
        :localized-description="localizedDescription"
        :localized-timeline="localizedTimeline"
        :localized-offers="localizedOffers"
        :localized-looking-for="localizedLookingFor"
        :page-url="currentUrl"
        @close="editDrawerOpen = false"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const route = useRoute()
const { t: $t, locale } = useI18n()
const localePath = useLocalePath()
const runtimeConfig = useRuntimeConfig()
const detailV2 = computed(() => Boolean(runtimeConfig.public?.detailV2))

const slugify = (text: string) =>
  text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 80)
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
const editDrawerOpen = ref(false)
const connectDrawerOpen = ref(false)

const projectSlug = computed(() => route.params.id as string)

// Current URL for sharing
const currentUrl = computed(() => {
  if (import.meta.client) {
    return window.location.href
  }
  return ''
})

// Fetch project — two-stage query to avoid loading all 848 projects.
// Stage 1: lightweight index (pubId + name only) to resolve slug → pubId.
// Stage 2: targeted single-row fetch by pubId.
const { data: project, error: projectError } = await useAsyncData(
  `project-${projectSlug.value}`,
  async () => {
    try {
      const nameIndex = await queryCollection('projects').select('pubId', 'name').all()
      const found = nameIndex.find((p: any) => {
        const name = typeof p.name === 'string' ? p.name : p.name?.en || ''
        return slugify(name) === projectSlug.value
      })

      if (!found) throw new Error('Project not found')

      const fullProject = await queryCollection('projects')
        .where('pubId', '=', found.pubId)
        .first()

      if (!fullProject) throw new Error('Project not found')
      return fullProject
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
  return proj.name?.en || proj.name?.[proj.originalLang || proj.lang] || Object.values(proj.name)[0] || ''
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

// Section nav: derived from data presence, in spec order
// (About, Video, Team, Timeline, Offers, Looking for)
const availableSections = computed(() => {
  const proj = project.value as any
  if (!proj) return []
  const list: { id: string; label: string }[] = []
  if (proj.entityDescription || localizedDescription.value)
    list.push({ id: 'about', label: $t('projects.detail.about') })
  if (proj.yt) list.push({ id: 'video', label: $t('projects.detail.video') })
  if (proj.team && proj.team.length > 0)
    list.push({ id: 'team', label: $t('projects.detail.team') })
  if (localizedTimeline.value.length > 0)
    list.push({ id: 'timeline', label: $t('projects.detail.timeline') })
  if (localizedOffers.value.length > 0)
    list.push({ id: 'offers', label: $t('projects.detail.offers') })
  if (localizedLookingFor.value.length > 0)
    list.push({ id: 'looking-for', label: $t('projects.detail.lookingFor') })
  return list
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
@use '~~/assets/styles/variables' as *;

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

/* Primary action bar — mobile/tablet only. Sits inside .detail-main
   after About. On desktop the right-rail sidebar already exposes
   Connect + Website + Edit + Share, so the inline duplicate is hidden. */
.action-bar {
  display: flex;
  gap: 6px;
  align-items: stretch;
  margin: 0 0 $rhythm-3;

  @media (min-width: $detail-bp-desktop) {
    display: none;
  }

  .action-connect {
    flex: 1 1 auto;
    min-width: 0;
  }

  .action-website {
    flex: 0 0 auto;
  }
}

.construction-banner {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.625rem 1rem;
  background: $saffron-pale;
  border-top: 1px solid $saffron;
  border-bottom: 1px solid $saffron;
  color: $saffron-dark;
  font-size: 0.9375rem;
  margin-top: $rhythm-2;

  @media (max-width: $detail-bp-tablet - 1) {
    margin-top: 8px;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    padding: 6px 12px;
    font-size: 0.8125rem;
    gap: 6px;
  }

  .construction-icon {
    color: $saffron-dark;
    flex-shrink: 0;
  }

  .construction-text {
    flex: 1;
    line-height: 1.45;
  }

  .construction-link {
    font-weight: 600;
    text-decoration: underline;
    cursor: pointer;
    margin-left: 0.25rem;
    color: inherit;

    &:hover {
      color: $clay;
    }

    &:focus-visible {
      outline: 2px solid $saffron-dark;
      outline-offset: 2px;
      border-radius: 2px;
    }
  }
}

.detail-grid {
  display: grid;
  grid-template-columns: minmax(0, 8fr) minmax(0, 4fr);
  gap: $gutter-desktop;
  max-width: $container-max-detail;
  margin: 0 auto;
  padding: $rhythm-4 $gutter-desktop;
}

.detail-main {
  grid-column: 1;
  min-width: 0;
}

.detail-sidebar-column {
  grid-column: 2;
  display: flex;
  flex-direction: column;
  gap: $rhythm-3;
  min-width: 0;
}

@media (max-width: $detail-bp-desktop - 1) {
  .detail-grid {
    grid-template-columns: 1fr;
    padding: $rhythm-2 $gutter-mobile $rhythm-3;
    gap: $rhythm-3;
  }

  .detail-main,
  .detail-sidebar-column {
    grid-column: 1;
  }

  /* Sidebar + related lives BELOW content on mobile — main content is
     what the user came for; key facts and related are supplementary. */
  .detail-sidebar-column {
    order: 1;
  }
}

/* The sidebar's share-strip carries share on every viewport now —
   the in-flow ProjectShare is fully redundant. */
.share-mobile-fallback {
  display: none;
}
</style>
