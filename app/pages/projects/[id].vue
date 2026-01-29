<template>
  <div class="project-detail">
    <!-- Loading state -->
    <div v-if="!project && !projectError" class="loading-container">
      <div class="loading-spinner" />
      <p>Loading project...</p>
    </div>

    <!-- Project content -->
    <div v-else-if="project" class="project-container">
      <!-- Translation Disclaimer -->
      <TranslationDisclaimer
        v-if="(project as any).originalLang && showDisclaimer"
        :original-lang="(project as any).originalLang"
        :current-locale="currentLocale"
        :showing-original="showOriginal"
        @toggle-original="toggleOriginal"
      />

      <!-- Header -->
      <div class="project-header">
        <div class="container">
          <div class="header-content">
            <div class="project-logo">
              {{ getInitials(localizedName) }}
            </div>
            <div class="header-info">
              <h1 class="project-name">{{ localizedName }}</h1>
              <div v-if="project.location" class="location">
                <i class="fas fa-map-marker-alt" />
                {{ project.location }}
              </div>
              <div class="tags">
                <span v-if="project.status" class="tag">
                  {{ getStatusLabel(String(project.status)) }}
                </span>
                <span v-if="project.continent?.length" class="tag">
                  {{ getContinentLabel(project.continent[0]) }}
                </span>
              </div>
              <div v-if="project.url" class="social-links">
                <a
                  :href="project.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label="Website"
                >
                  <i class="fas fa-globe" />
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- About Section -->
      <div class="section">
        <div class="container">
          <h2 class="section-title">
            <i class="fas fa-info-circle" />
            About {{ localizedName }}
          </h2>
          <div class="about-content">
            <p>{{ localizedDescription }}</p>
            <a
              v-if="project.url"
              :href="project.url"
              class="website-link"
              target="_blank"
              rel="noopener noreferrer"
            >
              <i class="fas fa-external-link-alt" /> Visit Website
            </a>
          </div>
        </div>
      </div>

      <!-- Video Section -->
      <div v-if="project.yt" class="section">
        <div class="container">
          <h2 class="section-title">
            <i class="fas fa-video" />
            {{ $t('project.video') }}
          </h2>
          <div class="video-container">
            <iframe
              :src="getYouTubeEmbedUrl(project.yt)"
              frameborder="0"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            />
          </div>
        </div>
      </div>

      <!-- Timeline/Milestones Section -->
      <div
        v-if="(project as any).timeline && Array.isArray((project as any).timeline)"
        class="section"
      >
        <div class="container">
          <h2 class="section-title">
            <i class="fas fa-flag-checkered" />
            Our Journey
          </h2>
          <div class="timeline">
            <div
              v-for="(milestone, index) in (project as any).timeline"
              :key="index"
              class="milestone"
            >
              <div class="milestone-date">{{ milestone.date }}</div>
              <div class="milestone-description">{{ milestone.text }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Products Section -->
      <div
        v-if="(project as any).products && Array.isArray((project as any).products)"
        class="section"
      >
        <div class="container">
          <h2 class="section-title">
            <i class="fas fa-box-open" />
            Products & Projects
          </h2>
          <div class="products-grid">
            <div
              v-for="(product, index) in (project as any).products"
              :key="index"
              class="product-card"
            >
              <div class="product-image">
                <div class="product-placeholder">{{ product.icon || '📦' }}</div>
              </div>
              <div class="product-content">
                <h3>{{ product.name }}</h3>
                <p>{{ product.description }}</p>
                <div v-if="product.tags" class="product-tags">
                  <span v-for="(tag, tagIndex) in product.tags" :key="tagIndex" class="product-tag">
                    {{ tag }}
                  </span>
                </div>
                <a
                  v-if="product.link"
                  :href="product.link"
                  class="product-link"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <i class="fas fa-arrow-right" /> Learn More
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Looking For / Offering Section -->
      <div v-if="(project as any).lookingFor || (project as any).offer" class="section">
        <div class="container">
          <div class="offerings-grid">
            <div
              v-if="(project as any).lookingFor && Array.isArray((project as any).lookingFor)"
              class="offerings-column"
            >
              <h3>
                <i class="fas fa-search" />
                Looking For
              </h3>
              <div class="offering-items">
                <div
                  v-for="(item, index) in (project as any).lookingFor"
                  :key="index"
                  class="offering-item"
                >
                  {{ item }}
                </div>
              </div>
            </div>
            <div
              v-if="(project as any).offer && Array.isArray((project as any).offer)"
              class="offerings-column"
            >
              <h3>
                <i class="fas fa-gift" />
                What We Offer
              </h3>
              <div class="offering-items">
                <div
                  v-for="(item, index) in (project as any).offer"
                  :key="index"
                  class="offering-item"
                >
                  {{ item }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Gallery Section -->
      <div
        v-if="(project as any).gallery && Array.isArray((project as any).gallery)"
        class="section"
      >
        <div class="container">
          <h2 class="section-title">
            <i class="fas fa-images" />
            Gallery
          </h2>
          <div class="gallery">
            <div
              v-for="(image, index) in (project as any).gallery"
              :key="index"
              class="gallery-item"
            >
              <img v-if="image" :src="image" :alt="`Gallery image ${index + 1}`" />
              <div v-else class="gallery-placeholder">📷</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Metadata Sidebar (Geography, Fields, Thematics, etc.) -->
      <div class="section metadata-section">
        <div class="container">
          <div class="metadata-grid">
            <!-- Geography -->
            <div v-if="project.continent?.length || project.country?.length" class="metadata-card">
              <h3>Geography</h3>
              <div v-if="project.continent?.length" class="metadata-group">
                <p class="metadata-label">Continents</p>
                <div class="tags-list">
                  <span
                    v-for="continentId in project.continent"
                    :key="continentId"
                    class="tag tag-sm"
                  >
                    {{ getContinentLabel(continentId) }}
                  </span>
                </div>
              </div>
              <div v-if="project.country?.length" class="metadata-group">
                <p class="metadata-label">Countries</p>
                <div class="tags-list">
                  <span v-for="countryId in project.country" :key="countryId" class="tag tag-sm">
                    {{ getCountryLabel(countryId) }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Fields -->
            <div v-if="project.field?.length" class="metadata-card">
              <h3>Research Fields</h3>
              <div class="tags-list">
                <span v-for="fieldId in project.field" :key="fieldId" class="tag tag-sm tag-blue">
                  {{ getFieldLabel(fieldId) }}
                </span>
              </div>
            </div>

            <!-- Thematics -->
            <div v-if="project.thematic?.length" class="metadata-card">
              <h3>Thematics</h3>
              <div class="tags-list">
                <span
                  v-for="thematicId in project.thematic"
                  :key="thematicId"
                  class="tag tag-sm tag-green"
                >
                  {{ getThematicLabel(thematicId) }}
                </span>
              </div>
            </div>

            <!-- Types -->
            <div v-if="project.type?.length" class="metadata-card">
              <h3>Types</h3>
              <div class="tags-list">
                <span v-for="typeId in project.type" :key="typeId" class="tag tag-sm tag-purple">
                  {{ getTypeLabel(typeId) }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Back button -->
      <div class="section">
        <div class="container">
          <div class="back-button-container">
            <NuxtLink :to="localePath('/projects')" class="btn btn-back">
              <i class="fas fa-arrow-left" /> Back to Projects
            </NuxtLink>
          </div>
        </div>
      </div>
    </div>

    <!-- Not found -->
    <div v-else class="not-found-container">
      <div class="not-found-content">
        <i class="fas fa-exclamation-circle not-found-icon" />
        <h2>Project Not Found</h2>
        <p>The project you're looking for doesn't exist or has been removed.</p>
        <NuxtLink :to="localePath('/projects')" class="btn btn-primary">
          Back to Projects
        </NuxtLink>
      </div>
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
  getStateLabel,
  getPeriodicityLabel
} = useProjectMappings()
const { isTranslated: checkIsTranslated } = useMultilingual()

// State for toggling between current locale and original language
const showOriginal = ref(false)

const projectId = computed(() => route.params.id as string)

// Fetch project
const { data: project, error: projectError } = await useAsyncData(
  `project-${projectId.value}`,
  async () => {
    try {
      const allProjects = await queryCollection('projects').all()

      // Try to find by pubId
      const foundByPubId = allProjects.find((p) => String(p.pubId) === String(projectId.value))
      if (foundByPubId) return foundByPubId

      // Try by stem as fallback
      const stemPath = `projects/${projectId.value}`
      const foundByStem = allProjects.find((p) => p.stem === stemPath)
      if (foundByStem) return foundByStem

      return null
    } catch (e) {
      console.error('Error loading project:', e)
      return null
    }
  }
)

// Helper to get initials from name
const getInitials = (name: string) => {
  if (!name) return '?'
  const words = name.split(' ')
  if (words.length >= 2) {
    return (words[0].charAt(0) + words[words.length - 1].charAt(0)).toUpperCase()
  }
  return name.charAt(0).toUpperCase()
}

// Extract YouTube video ID from various URL formats
const getYouTubeEmbedUrl = (urlOrId: string) => {
  if (!urlOrId.includes('/') && !urlOrId.includes('http')) {
    return `https://www.youtube.com/embed/${urlOrId}`
  }

  try {
    const urlObj = new URL(urlOrId)
    let videoId = ''

    if (urlObj.hostname.includes('youtube.com')) {
      videoId = urlObj.searchParams.get('v') || ''
    } else if (urlObj.hostname.includes('youtu.be')) {
      videoId = urlObj.pathname.slice(1)
    }

    return `https://www.youtube.com/embed/${videoId}`
  } catch {
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

const showDisclaimer = computed(() => {
  const proj = project.value as any
  return proj?.originalLang && proj.originalLang !== locale.value
})

// Toggle between original and translated version
const toggleOriginal = () => {
  showOriginal.value = !showOriginal.value
}

// SEO
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

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-detail {
  font-family: 'Playfair Display', serif;
  background-color: $cream;
  color: $brown-dark;
  min-height: 100vh;
}

.loading-container,
.not-found-container {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  padding: 4rem 2rem;
}

.loading-spinner {
  width: 64px;
  height: 64px;
  border: 4px solid $warm-beige;
  border-top-color: $green-bright;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.not-found-icon {
  font-size: 4rem;
  color: $green-bright;
  margin-bottom: 1rem;
}

.not-found-content {
  text-align: center;
  max-width: 500px;

  h2 {
    font-size: 2rem;
    font-weight: 700;
    color: $forest-green;
    margin-bottom: 1rem;
  }

  p {
    font-size: 1.1rem;
    margin-bottom: 2rem;
    line-height: 1.6;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.project-header {
  background-color: $warm-beige;
  padding: 4rem 0 3rem;
  margin-bottom: 0;
}

.header-content {
  display: flex;
  align-items: flex-start;
  gap: 2rem;
  flex-wrap: wrap;
}

.project-logo {
  width: 120px;
  height: 120px;
  background-color: $cream;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 700;
  border: 2px solid $green-bright;
  flex-shrink: 0;
  color: $green-bright;
}

.header-info {
  flex: 1;
  min-width: 250px;
}

.project-name {
  font-size: 2.5rem;
  font-weight: 700;
  color: $forest-green;
  margin-bottom: 0.75rem;
  line-height: 1.2;
}

.location {
  font-size: 1.2rem;
  color: $brown-dark;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}

.tag {
  background-color: $green-bright;
  color: $cream;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;

  &.tag-sm {
    padding: 0.375rem 0.875rem;
    font-size: 0.85rem;
  }

  &.tag-blue {
    background-color: #4a90e2;
  }

  &.tag-green {
    background-color: $green-bright;
  }

  &.tag-purple {
    background-color: #9b59b6;
  }
}

.social-links {
  display: flex;
  gap: 1rem;

  a {
    color: $forest-green;
    font-size: 1.5rem;
    transition: color 0.3s;
    text-decoration: none;

    &:hover {
      color: $green-bright;
    }
  }
}

.section {
  padding: 4rem 0;
  border-bottom: 1px solid $warm-beige;

  &:last-child {
    border-bottom: none;
  }
}

.section-title {
  font-size: 2rem;
  font-weight: 700;
  color: $forest-green;
  margin-bottom: 2rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;

  i {
    color: $green-bright;
  }
}

.about-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: $brown-dark;

  p {
    margin-bottom: 1.5rem;
  }
}

.website-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: $green-bright;
  text-decoration: none;
  font-weight: 600;
  margin-top: 1.25rem;
  font-size: 1.1rem;
  transition: color 0.3s;

  &:hover {
    color: $forest-green;
  }
}

.video-container {
  position: relative;
  padding-bottom: 56.25%;
  height: 0;
  overflow: hidden;
  border-radius: 12px;
  background-color: $warm-beige;
  box-shadow: 0 4px 12px rgba(44, 36, 22, 0.1);

  iframe {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
  }
}

.timeline {
  position: relative;
  padding-left: 2.5rem;

  &::before {
    content: '';
    position: absolute;
    left: 15px;
    top: 0;
    bottom: 0;
    width: 3px;
    background-color: $green-bright;
  }
}

.milestone {
  position: relative;
  margin-bottom: 2rem;

  &::before {
    content: '';
    position: absolute;
    left: -33px;
    top: 5px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: $green-bright;
    border: 3px solid $cream;
  }
}

.milestone-date {
  font-weight: 700;
  color: $forest-green;
  font-size: 1.1rem;
  margin-bottom: 0.25rem;
}

.milestone-description {
  color: $brown-dark;
  line-height: 1.6;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.75rem;
}

.product-card {
  background-color: $warm-beige;
  border-radius: 12px;
  overflow: hidden;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  border: 2px solid $green-bright;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 20px rgba(76, 160, 73, 0.2);
  }
}

.product-image {
  background-color: $cream;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 150px;
}

.product-placeholder {
  font-size: 4rem;
  color: $green-bright;
}

.product-content {
  padding: 1.5rem;

  h3 {
    color: $forest-green;
    font-size: 1.3rem;
    margin-bottom: 0.75rem;
    font-weight: 700;
  }

  p {
    color: $brown-dark;
    line-height: 1.6;
    margin-bottom: 1rem;
  }
}

.product-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.product-tag {
  background-color: $green-bright;
  color: $cream;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.product-link {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  color: $green-bright;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: color 0.3s;

  &:hover {
    color: $forest-green;
  }
}

.offerings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.offerings-column {
  h3 {
    color: $forest-green;
    font-size: 1.5rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    i {
      color: $green-bright;
    }
  }
}

.offering-items {
  display: flex;
  flex-wrap: wrap;
  gap: 0.875rem;
}

.offering-item {
  background-color: $warm-beige;
  padding: 0.75rem 1.25rem;
  border-radius: 8px;
  border: 2px solid $green-bright;
  font-size: 1rem;
  color: $brown-dark;
}

.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.25rem;
}

.gallery-item {
  aspect-ratio: 1;
  background-color: $warm-beige;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(44, 36, 22, 0.1);
  cursor: pointer;
  transition: transform 0.3s;

  &:hover {
    transform: scale(1.05);
  }

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
}

.gallery-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: $green-bright;
}

.metadata-section {
  background-color: $warm-beige;
  padding: 3rem 0;
}

.metadata-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.metadata-card {
  background-color: $cream;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid $green-bright;

  h3 {
    color: $forest-green;
    font-size: 1.2rem;
    font-weight: 700;
    margin-bottom: 1rem;
  }
}

.metadata-group {
  margin-bottom: 1.25rem;

  &:last-child {
    margin-bottom: 0;
  }
}

.metadata-label {
  font-weight: 600;
  color: $forest-green;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
}

.tags-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.back-button-container {
  text-align: center;
}

.btn {
  padding: 0.875rem 1.875rem;
  border: 2px solid $green-bright;
  background-color: transparent;
  color: $brown-dark;
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 50px;
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    background-color: $green-bright;
    color: $cream;
  }

  &.btn-primary {
    background-color: $green-bright;
    color: $cream;

    &:hover {
      background-color: $forest-green;
      border-color: $forest-green;
    }
  }

  &.btn-back {
    i {
      font-size: 0.875rem;
    }
  }
}

@media (max-width: 768px) {
  .project-name {
    font-size: 2rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .project-logo {
    width: 100px;
    height: 100px;
    font-size: 2.5rem;
  }

  .products-grid,
  .metadata-grid {
    grid-template-columns: 1fr;
  }
}
</style>
