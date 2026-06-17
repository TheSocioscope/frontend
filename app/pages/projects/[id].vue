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
      <!-- Breadcrumb -->
      <ProjectBreadcrumb
        :localized-name="localizedName"
        :page-url="currentUrl"
      />

      <div class="project-body">
        <!-- Hero: tags + title + entity + actions -->
        <ProjectHeader
          :project="project"
          :localized-name="localizedName"
          :localized-description="localizedTagline"
          @connect="connectDrawerOpen = true"
          @edit="editDrawerOpen = true"
        />

        <!-- Photos & Videos (video embed + photo grid, unified) -->
        <ProjectGallery
          :yt="project.yt"
          :video-date="project.videoDate"
          :localized-gallery="localizedGallery"
          @edit="editDrawerOpen = true"
        />

        <!-- À propos -->
        <template v-if="localizedDescription">
          <hr class="dvd" />
          <div class="about-section">
            <span class="section-label">{{ $t('projects.detail.about') }}</span>
            <div class="about-content" v-html="processedDescription" />
          </div>
        </template>

        <!-- Team (after About, before Exchange) -->
        <template v-if="project.team && project.team.length > 0">
          <hr class="dvd" />
          <ProjectTeam :project="project" />
        </template>

        <!-- Exchange board: offers + looking-for side by side -->
        <template v-if="localizedOffers.length || localizedLookingFor.length">
          <hr class="dvd" />
          <div class="exchange-section">
            <span class="section-label">{{ $t('projects.detail.exchange', 'Exchange board') }}</span>
            <div class="exchange-grid">
              <ProjectOffers
                v-if="localizedOffers.length"
                :localized-offers="localizedOffers"
                :localized-name="localizedName"
                :column="true"
              />
              <ProjectLookingFor
                v-if="localizedLookingFor.length"
                :localized-looking-for="localizedLookingFor"
                :localized-name="localizedName"
                :column="true"
                @connect="connectDrawerOpen = true"
              />
            </div>
          </div>
        </template>

        <!-- Timeline -->
        <hr class="dvd" />
        <template v-if="localizedTimeline && localizedTimeline.length > 0">
          <ProjectTimeline :localized-timeline="localizedTimeline" />
        </template>
        <template v-else>
          <section class="project-timeline-empty">
            <span class="section-label">{{ $t('projects.detail.timeline') }}</span>
            <div class="empty-state">
              <v-icon size="48" color="#4ca049">mdi-calendar-blank-outline</v-icon>
              <h3>{{ $t('projects.detail.noTimeline', 'No journey yet') }}</h3>
              <p>{{ $t('projects.detail.noTimelineHint', 'Help us document this initiative\'s timeline') }}</p>
              <button class="edit-btn" @click="editDrawerOpen = true">
                <v-icon size="small">mdi-pencil-outline</v-icon>
                {{ $t('projects.detail.suggestEdit', 'Suggest an edit') }}
              </button>
            </div>
          </section>
        </template>

        <!-- Similar initiatives -->
        <ProjectRelated :current-project="project" />
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
        :localized-tagline="localizedTagline"
        :localized-description="localizedDescription"
        :localized-timeline="localizedTimeline"
        :localized-offers="localizedOffers"
        :localized-looking-for="localizedLookingFor"
        :page-url="currentUrl"
        @close="editDrawerOpen = false"
      />

      <!-- Action FABs (Contact, Edit, Share) -->
      <div class="floating-actions">
        <button
          class="floating-fab floating-fab--contact"
          :aria-label="$t('projects.detail.connect', 'Contact')"
          @click="connectDrawerOpen = true"
        >
          <v-icon size="20">mdi-email-outline</v-icon>
        </button>
        <button
          class="floating-fab floating-fab--edit"
          :aria-label="$t('projects.detail.suggestEdit', 'Suggest an edit')"
          @click="editDrawerOpen = true"
        >
          <v-icon size="20">mdi-pencil-outline</v-icon>
        </button>
        <button
          class="floating-fab floating-fab--share"
          :aria-label="$t('projects.detail.share', 'Share')"
        >
          <v-icon size="20">mdi-share-variant</v-icon>
        </button>
      </div>
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

const SITE_URL = 'https://thesocioscope.org'

// Canonical URL — constructed server-side so it's present during SSR/build
const currentUrl = computed(() => `${SITE_URL}/projects/${projectSlug.value}/`)

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
  const raw = proj.description?.[currentLocale.value] || proj.description?.en || ''
  return typeof raw === 'string' ? raw : ''
})

const localizedTagline = computed(() => {
  const proj = project.value as any
  if (!proj) return ''
  const t = proj.tagline
  if (!t) return ''
  if (typeof t === 'string') return t
  return t[currentLocale.value] || t.en || ''
})

// Convert plain-text newlines to HTML paragraphs for the about section
const processedDescription = computed(() => {
  const desc = localizedDescription.value
  if (!desc) return ''
  // If it already contains HTML tags, return as-is
  if (/<[a-z][\s\S]*>/i.test(desc)) return desc
  // Split on double newlines → paragraphs; single newlines → <br>
  return desc
    .trim()
    .split(/\n\n+/)
    .map((p) => `<p>${p.replace(/\n/g, '<br>')}</p>`)
    .join('')
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
    title:
      typeof item.title === 'string'
        ? item.title
        : item.title?.[currentLocale.value] || item.title?.en || '',
    text:
      typeof item.text === 'string'
        ? item.text
        : item.text?.[currentLocale.value] || item.text?.en || '',
    summary:
      typeof item.summary === 'string'
        ? item.summary
        : item.summary?.[currentLocale.value] || item.summary?.en || ''
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
  if (proj.yt || localizedGallery.value.length > 0)
    list.push({ id: 'gallery', label: $t('projects.detail.video') })
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
      link: [{ rel: 'canonical', href: currentUrl.value }],
      meta: [
        { name: 'description', content: localizedDescription.value },
        { property: 'og:title', content: localizedName.value },
        { property: 'og:description', content: localizedDescription.value },
        { property: 'og:type', content: 'website' },
        { property: 'og:url', content: currentUrl.value },
        { property: 'og:site_name', content: 'The Socioscope' }
      ],
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'ItemPage',
            name: localizedName.value,
            description: localizedDescription.value,
            url: currentUrl.value,
            isPartOf: { '@type': 'WebSite', name: 'The Socioscope', url: SITE_URL },
            ...(project.value.country?.length
              ? { spatialCoverage: { '@type': 'Place', addressCountry: project.value.country[0] } }
              : {})
          })
        }
      ]
    })
  }
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-detail {
  min-height: 100vh;
  background: $surface-page;
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

/* Single-column content body, centred at 860px */
.project-body {
  max-width: 860px;
  margin: 0 auto;
  padding: $rhythm-4 $gutter-desktop $rhythm-12;

  @media (max-width: $detail-bp-tablet - 1) {
    padding: $rhythm-2 $gutter-mobile $rhythm-8;
  }
}

/* Thin section divider */
.dvd {
  border: none;
  border-top: 0.5px solid $border-soft;
  margin: $rhythm-4 0;
}

/* Small-caps section label (shared across inline sections) */
.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $text-secondary;
  margin-bottom: $rhythm-2;
}

/* À propos */
.about-section {
  margin-bottom: $rhythm-6;
}

.about-content {
  font-size: 14px;
  line-height: 1.75;
  color: $text-secondary;

  :deep(p) {
    margin-bottom: $rhythm-2;
  }

  :deep(p:last-child) {
    margin-bottom: 0;
  }

  :deep(ul),
  :deep(ol) {
    margin-left: $rhythm-3;
    margin-bottom: $rhythm-2;
  }
}

/* Exchange board */
.exchange-section {
  margin-bottom: $rhythm-6;
}

.exchange-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: $rhythm-4;

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: 1fr;
    gap: $rhythm-3;
  }
}

/* Floating Action Buttons */
.floating-actions {
  position: fixed;
  bottom: 1.5rem;
  right: 1.5rem;
  z-index: $z-dropdown;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.floating-fab {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: scale(1.1);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
  }

  &:focus-visible {
    outline: 2px solid white;
    outline-offset: 3px;
  }

  &--contact {
    background: #85C49A; /* pastel green */

    &:hover {
      background: #7ab88b;
    }
  }

  &--edit {
    background: #E8C47A; /* pastel orange */

    &:hover {
      background: #ddb866;
    }
  }

  &--share {
    background: #C4A890; /* pastel brown */

    &:hover {
      background: #b89a7f;
    }
  }
}

/* Empty timeline state */
.project-timeline-empty {
  margin-bottom: $rhythm-4;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $rhythm-2;
}

.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $text-secondary;
  margin-bottom: $rhythm-2;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 3rem 2rem;
  background: rgba(76, 160, 73, 0.05);
  border: 1px dashed rgba(76, 160, 73, 0.3);
  border-radius: 10px;
  text-align: center;

  h3 {
    font-size: 1rem;
    font-weight: 600;
    color: $earth-90;
    margin: 0;
  }

  p {
    font-size: 0.875rem;
    color: $text-secondary;
    margin: 0;
  }
}

.edit-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: $green-forest;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  font-family: $font-family-base;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;

  &:hover {
    background: $green-leaf;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

</style>
