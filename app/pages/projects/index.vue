<template>
  <div>
    <PageHero
      :title="$t('projects.hero.title')"
      :subtitle="$t('projects.hero.subtitle')"
      icon="mdi-sprout"
      compact
      centered
    >
      <template v-if="hasActiveFilters" #cta>
        <button type="button" class="clear-all-btn" @click="resetFilters">
          <v-icon size="small">mdi-close-circle-outline</v-icon>
          {{ $t('projects.clearAllFilters', 'Clear all filters') }}
        </button>
      </template>
    </PageHero>

    <section class="section">
      <div class="container">
        <!-- Filters: compact horizontal row (desktop) + collapse-to-button (mobile).
             Sort props let the Customize sheet host sort on mobile so the page
             doesn't waste a toolbar row on it. -->
        <ProjectsFilters
          :filters="filters"
          :continent-options="continentOptions"
          :country-options="countryOptions"
          :status-options="statusOptions"
          :role-options="roleOptions"
          :biz-model-options="bizModelOptions"
          :size-options="sizeOptions"
          :geo-reach-options="geoReachOptions"
          :sector-options="sectorOptions"
          :resource-type-options="resourceTypeOptions"
          :sort-by="sortBy"
          :sort-order="sortOrder"
          :sort-options="sortOptions"
          class="filters-bar"
          @update:model-value="filters = $event"
          @update:sort-by="sortBy = $event"
          @update:sort-order="sortOrder = $event"
          @reset="resetFilters"
        />

        <!-- Toolbar: sort (desktop only — mobile uses the Customize sheet) +
             view toggle as a segmented control on a single row -->
        <div class="toolbar-row">
          <ListControls
            v-if="!isMobile"
            v-model:sort-by="sortBy"
            v-model:sort-order="sortOrder"
            v-model:items-per-page="itemsPerPage"
            :sort-options="sortOptions"
            :per-page-options="[12, 24, 36, 48]"
            :sort-label="$t('projects.sortBy')"
            :per-page-label="$t('projects.perPage')"
            :show-per-page="!isMobile"
          />
          <div
            class="view-toggle segmented"
            role="group"
            :aria-label="$t('projects.viewMode', 'View mode')"
          >
            <button
              class="view-btn"
              :class="{ active: viewMode === 'grid' }"
              :aria-pressed="viewMode === 'grid'"
              :aria-label="$t('projects.gridView', 'Grid view')"
              @click="viewMode = 'grid'"
            >
              <v-icon size="small">mdi-view-grid-outline</v-icon>
              <span class="btn-label">{{ $t('projects.gridView', 'Grid') }}</span>
            </button>
            <button
              class="view-btn"
              :class="{ active: viewMode === 'list' }"
              :aria-pressed="viewMode === 'list'"
              :aria-label="$t('projects.listView', 'List view')"
              @click="viewMode = 'list'"
            >
              <v-icon size="small">mdi-view-list-outline</v-icon>
              <span class="btn-label">{{ $t('projects.listView', 'List') }}</span>
            </button>
            <button
              class="view-btn"
              :class="{ active: viewMode === 'map' }"
              :aria-pressed="viewMode === 'map'"
              :aria-label="$t('projects.mapView', 'Map view')"
              @click="viewMode = 'map'"
            >
              <v-icon size="small">mdi-map-outline</v-icon>
              <span class="btn-label">{{ $t('projects.mapView', 'Map') }}</span>
            </button>
          </div>
        </div>

        <!-- Map view: desktop pairs a clickable country sidebar with the map.
             Click a country in the list → map zooms to it. The checkbox
             toggles the country in the filter set. Mobile shows just the map. -->
        <div v-if="viewMode === 'map'" class="projects-map-wrap">
          <div class="map-layout section-reveal">
            <aside
              v-if="!isMobile"
              class="map-sidebar"
              :aria-label="$t('projects.countryFilter', 'Country filter')"
            >
              <div class="sidebar-search">
                <v-icon size="small" class="search-icon">mdi-magnify</v-icon>
                <input
                  v-model="countrySearch"
                  type="text"
                  :placeholder="$t('projects.searchCountries', 'Search countries')"
                  class="search-input"
                />
                <button
                  v-if="countrySearch"
                  type="button"
                  class="search-clear"
                  :aria-label="$t('common.clear', 'Clear')"
                  @click="countrySearch = ''"
                >
                  <v-icon size="x-small">mdi-close</v-icon>
                </button>
              </div>
              <ul class="sidebar-list country-list">
                <li v-for="c in visibleSidebarCountries" :key="c.code">
                  <button
                    type="button"
                    class="country-row"
                    :class="{ selected: filters.selectedCountries.includes(c.code) }"
                    @click="onCountryRowClick(c.code)"
                  >
                    <span
                      class="country-checkbox"
                      :class="{ checked: filters.selectedCountries.includes(c.code) }"
                      :aria-hidden="true"
                    >
                      <v-icon
                        v-if="filters.selectedCountries.includes(c.code)"
                        size="14"
                      >mdi-check</v-icon>
                    </span>
                    <span class="country-name">{{ getCountryLabel(c.code) }}</span>
                  </button>
                </li>
                <li v-if="!visibleSidebarCountries.length" class="country-empty">
                  {{ $t('projects.noCountriesMatch', 'No countries match') }}
                </li>
              </ul>
              <footer
                v-if="filters.selectedCountries.length"
                class="sidebar-actions"
              >
                <button
                  type="button"
                  class="reset-countries"
                  @click="filters.selectedCountries = []"
                >
                  <v-icon size="small">mdi-close-circle-outline</v-icon>
                  {{ $t('projects.clearCountries', 'Clear country selection') }}
                </button>
              </footer>
            </aside>

            <div class="map-area">
              <ClientOnly>
                <ProjectsMapView
                  ref="mapViewRef"
                  :filtered-ids="filteredIds"
                  @select-country="onSelectCountry"
                />
                <template #fallback>
                  <div class="map-fallback">
                    <v-progress-circular indeterminate size="32" />
                  </div>
                </template>
              </ClientOnly>
            </div>
          </div>
        </div>

        <!-- Grid view (desktop + mobile share the same markup; mobile uses
             lazy-loaded displayedProjects, desktop uses paginatedProjects) -->
        <div
          v-else-if="filteredProjects.length > 0 && viewMode === 'grid'"
          class="projects-grid section-reveal"
        >
          <ProjectsCard
            v-for="project in isMobile ? displayedProjects : paginatedProjects"
            :key="project.pubId"
            :project="project"
            @click="handleProjectClick"
          />
        </div>

        <!-- List view (desktop + mobile) -->
        <div
          v-else-if="filteredProjects.length > 0 && viewMode === 'list'"
          class="projects-list section-reveal"
        >
          <a
            v-for="project in isMobile ? displayedProjects : paginatedProjects"
            :key="project.pubId"
            :href="getProjectUrl(project)"
            class="project-row"
            @click="handleProjectClick(project, $event)"
          >
            <div class="row-avatar" :style="{ background: getRowBackground(project) }">
              {{ getRowInitials(project) }}
            </div>
            <div class="row-body">
              <h3 class="row-name">{{ getRowName(project) }}</h3>
              <p v-if="getRowDescription(project)" class="row-description">
                {{ getRowDescription(project) }}
              </p>
              <p v-else-if="project.location" class="row-location">
                <v-icon size="x-small">mdi-map-marker</v-icon> {{ project.location }}
              </p>
            </div>
            <div class="row-tags">
              <v-chip
                v-for="c in project.continent?.slice(0, 2) || []"
                :key="c"
                size="x-small"
                class="mr-1"
              >{{ getContinentLabel(c) }}</v-chip>
            </div>
            <v-icon class="row-arrow">mdi-chevron-right</v-icon>
          </a>
        </div>

        <!-- Empty state (skipped in map view; map renders its own empty panel) -->
        <div v-else-if="viewMode !== 'map'" class="empty-state section-reveal">
          <p>{{ $t('projects.noProjects', 'No projects found') }}</p>
        </div>

        <!-- Desktop Pagination (map view doesn't paginate) -->
        <ListPagination
          v-if="viewMode !== 'map' && !isMobile && totalPages > 1"
          :current-page="currentPage"
          :total-pages="totalPages"
          :previous-label="$t('projects.pagination.previous')"
          :next-label="$t('projects.pagination.next')"
          @prev="prevPage"
          @next="nextPage"
          @goto="goToPage"
        />

        <!-- Mobile Load More (skipped in map view) -->
        <ListLoadMore
          v-if="viewMode !== 'map' && isMobile"
          :has-more="hasMoreProjects"
          :label="$t('projects.loadMore')"
          @load-more="loadMoreProjects"
        />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const localePath = useLocalePath()
const route = useRoute()
const router = useRouter()
const { getContinentLabel, getCountryLabel, getStatusLabel } = useProjectMappings()

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
  selectedRoles: [] as string[],
  selectedBizModels: [] as string[],
  selectedSizes: [] as string[],
  selectedGeoReach: [] as string[],
  selectedSectors: [] as string[],
  selectedResourceTypes: [] as string[]
})

// Persist the user's filter selections so they survive navigating away and
// back (and page reloads) until they explicitly clear them. The URL query
// still takes priority for deep/shared links; localStorage is the fallback.
const FILTERS_STORAGE_KEY = 'projects:filters'

const currentPage = ref(1)
const itemsPerPage = ref(12)
const sortBy = ref('name')
const sortOrder = ref<'asc' | 'desc'>('asc')
const shuffleIndex = ref<Map<number, number>>(new Map())
const viewMode = ref<'grid' | 'list' | 'map'>('grid')

const onSelectCountry = (code: string) => {
  if (!filters.value.selectedCountries.includes(code)) {
    filters.value = {
      ...filters.value,
      selectedCountries: [...filters.value.selectedCountries, code]
    }
  }
}

// Sidebar country filter state — clicking a row zooms the map; clicking
// the checkbox toggles the country in the filter set.
const mapViewRef = ref<{ zoomToCountry?: (code: string) => void } | null>(null)
const countrySearch = ref('')

const onCountryRowClick = (code: string) => {
  // Multi-select: tapping a row toggles the country in the filter set
  // and zooms the map to it. Selected countries stay highlighted; tap
  // again to deselect (the checkbox visualises state but the row is the
  // primary tap target).
  toggleCountryFilter(code)
  // Defer the zoom so the filter recompute settles first.
  nextTick(() => {
    mapViewRef.value?.zoomToCountry?.(code)
  })
}

const toggleCountryFilter = (code: string) => {
  const list = filters.value.selectedCountries
  filters.value = {
    ...filters.value,
    selectedCountries: list.includes(code)
      ? list.filter((c) => c !== code)
      : [...list, code]
  }
}
const isMobile = ref(false)
const mobileDisplayCount = ref(12)

const sortOptions = [
  { value: 'score', label: $t('projects.sort.score') },
  { value: 'name', label: $t('projects.sort.name') },
  { value: 'createdAt', label: $t('projects.sort.date') }
]

// Detect mobile/desktop and switch view mode accordingly
onMounted(() => {
  isMobile.value = window.innerWidth < 768
  // Set default view mode based on device
  if (isMobile.value) {
    viewMode.value = 'list'
  } else {
    viewMode.value = 'grid'
  }
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth < 768
    // Switch view mode when crossing breakpoint
    if (isMobile.value && viewMode.value === 'grid') {
      viewMode.value = 'list'
    } else if (!isMobile.value && viewMode.value === 'list') {
      viewMode.value = 'grid'
    }
  })

  // Build a random shuffle order once per page load
  if (projectsData.value) {
    const ids = (projectsData.value as any[]).map((p) => p.pubId)
    const shuffled = [...ids].sort(() => Math.random() - 0.5)
    shuffleIndex.value = new Map(shuffled.map((id, i) => [id, i]))
  }

  const q = route.query
  const hasQueryFilters = Boolean(
    q.countries || q.continent || q.status || q.roles || q.bizModels ||
    q.sizes || q.geoReach || q.sectors || q.resourceTypes
  )

  if (hasQueryFilters) {
    const { countries, continent, status, roles, bizModels, sizes, geoReach, sectors, resourceTypes } =
      q

    if (countries)
      filters.value.selectedCountries = Array.isArray(countries) ? countries : [countries as string]
    if (continent) filters.value.selectedContinent = continent as string
    if (status) filters.value.selectedStatus = status as string
    if (roles)
      filters.value.selectedRoles = Array.isArray(roles) ? roles : [roles as string]
    if (bizModels)
      filters.value.selectedBizModels = Array.isArray(bizModels) ? bizModels : [bizModels as string]
    if (sizes)
      filters.value.selectedSizes = Array.isArray(sizes) ? sizes : [sizes as string]
    if (geoReach)
      filters.value.selectedGeoReach = Array.isArray(geoReach) ? geoReach : [geoReach as string]
    if (sectors)
      filters.value.selectedSectors = Array.isArray(sectors) ? sectors : [sectors as string]
    if (resourceTypes)
      filters.value.selectedResourceTypes = Array.isArray(resourceTypes)
        ? resourceTypes
        : [resourceTypes as string]
  } else {
    // No filters in the URL (e.g. arrived via the nav menu or a back-link) —
    // restore the last saved selection so the user's choices persist across
    // navigation and reloads until they clear them.
    try {
      const raw = localStorage.getItem(FILTERS_STORAGE_KEY)
      if (raw) filters.value = { ...filters.value, ...JSON.parse(raw) }
    } catch {
      // ignore unavailable or corrupt storage
    }
  }
})

const toggleSortOrder = () => {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
}

// Update URL when filters change
watch(
  filters,
  () => {
    const query: Record<string, string | string[]> = {}

    if (filters.value.selectedCountries.length) query.countries = filters.value.selectedCountries
    if (filters.value.selectedContinent) query.continent = filters.value.selectedContinent
    if (filters.value.selectedStatus) query.status = filters.value.selectedStatus
    if (filters.value.selectedRoles.length) query.roles = filters.value.selectedRoles
    if (filters.value.selectedBizModels.length) query.bizModels = filters.value.selectedBizModels
    if (filters.value.selectedSizes.length) query.sizes = filters.value.selectedSizes
    if (filters.value.selectedGeoReach.length) query.geoReach = filters.value.selectedGeoReach
    if (filters.value.selectedSectors.length) query.sectors = filters.value.selectedSectors
    if (filters.value.selectedResourceTypes.length)
      query.resourceTypes = filters.value.selectedResourceTypes

    router.push({ query })

    // Persist selections so they survive navigation + reloads until cleared.
    try {
      if (hasActiveFilters.value) {
        localStorage.setItem(FILTERS_STORAGE_KEY, JSON.stringify(filters.value))
      } else {
        localStorage.removeItem(FILTERS_STORAGE_KEY)
      }
    } catch {
      // storage unavailable (e.g. private mode) — URL sync still applies
    }
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

// Fixed option lists for entity coding filters
const roleOptions = [
  'Primary Production',
  'Transformation/Processing',
  'Distribution/Logistics',
  'Retail',
  'Food Service/Hospitality',
  'Waste & Circular Economy',
  'Support Services',
  'Finance & Investment',
  'Governance & Regulation',
  'Civil Society & Networks',
  'Other Role'
]

const bizModelOptions = [
  'For-profit private',
  'Cooperative/mutual',
  'Social enterprise',
  'Non-profit/charity',
  'Public body',
  'Public-private partnership',
  'Individual/informal',
  'Other model'
]

const sizeOptions = [
  'Individual/Solo',
  'Micro',
  'Small',
  'Medium',
  'Large',
  'Very Large',
  'Unknown'
]

const geoReachOptions = ['Local', 'Regional', 'National', 'International', 'Unknown']

const sectorOptions = [
  'Agriculture/Agroecology',
  'Fisheries & Aquaculture',
  'Livestock & Dairy',
  'Food Processing/Products',
  'Distribution & Logistics',
  'Waste & Circular Economy',
  'Energy',
  'Water',
  'Technology & Innovation',
  'Health & Nutrition',
  'Environment & Biodiversity',
  'Policy & Advocacy',
  'Social & Community',
  'Other sector'
]

const resourceTypeOptions = [
  'Goods & Products',
  'Services',
  'Financial',
  'Access & Infrastructure',
  'Knowledge & Information',
  'Licences & Permissions',
  'Restriction & Obligation',
  'Support & Endorsement',
  'Other resource'
]

// Filtered projects
// Pub-ids of currently-filtered projects — feeds the Map view's color
// intensity so it reacts to filters in real time.
// True if the user has any filter active — search, geography, or any
// of the entity-coding facets. Drives the "Clear all filters" button
// in the title bar (only visible when there's something to clear).
const hasActiveFilters = computed(() => {
  const f = filters.value
  return Boolean(
    f.searchQuery ||
      f.selectedContinent ||
      f.selectedStatus ||
      f.selectedCountries.length ||
      f.selectedRoles.length ||
      f.selectedBizModels.length ||
      f.selectedSizes.length ||
      f.selectedGeoReach.length ||
      f.selectedSectors.length ||
      f.selectedResourceTypes.length
  )
})

const filteredIds = computed<number[]>(() => filteredProjects.value.map((p) => p.pubId))

// Project set with every filter EXCEPT the country selection applied.
// The sidebar country list reads from this so the user can keep adding
// countries to the multi-select without the list collapsing to only the
// already-selected ones.
const projectsForCountryList = computed(() => {
  let filtered = projects.value.filter((p) => !p.removedAt)
  const f = filters.value

  if (f.searchQuery) {
    const normalize = (s: string) =>
      s
        .normalize('NFD')
        .replace(/[̀-ͯ]/g, '')
        .toLowerCase()
    const query = normalize(f.searchQuery)
    filtered = filtered.filter((p) => {
      const getText = (field: any): string => {
        if (!field) return ''
        if (typeof field === 'string') return normalize(field)
        if (typeof field === 'object') {
          return Object.values(field)
            .filter((v) => typeof v === 'string')
            .map((v) => normalize(v as string))
            .join(' ')
        }
        return ''
      }
      return (
        getText(p.name).includes(query) ||
        getText(p.description).includes(query) ||
        normalize(p.location || '').includes(query)
      )
    })
  }

  if (f.selectedContinent) {
    filtered = filtered.filter((p) => p.continent?.includes(f.selectedContinent))
  }
  // NB: selectedCountries deliberately NOT applied here.
  if (f.selectedStatus) {
    filtered = filtered.filter((p) => p.status === f.selectedStatus)
  }
  if (f.selectedRoles.length) {
    filtered = filtered.filter((p) =>
      p.entityRole?.some((r: string) => f.selectedRoles.includes(r))
    )
  }
  if (f.selectedBizModels.length) {
    filtered = filtered.filter((p) => p.bizModel && f.selectedBizModels.includes(p.bizModel))
  }
  if (f.selectedSizes.length) {
    filtered = filtered.filter((p) => p.entitySize && f.selectedSizes.includes(p.entitySize))
  }
  if (f.selectedGeoReach.length) {
    filtered = filtered.filter((p) => p.geoReach && f.selectedGeoReach.includes(p.geoReach))
  }
  if (f.selectedSectors.length) {
    filtered = filtered.filter((p) =>
      p.sectorFocus?.some((s: string) => f.selectedSectors.includes(s))
    )
  }
  if (f.selectedResourceTypes.length) {
    filtered = filtered.filter(
      (p) => p.resourceType && f.selectedResourceTypes.includes(p.resourceType)
    )
  }
  return filtered
})

// Aggregate per-country counts from the filter-minus-country project set,
// so picking one country doesn't collapse the rest of the list. The sidebar
// list reads from this — sorted alphabetically by the (localized) country name.
const activeCountriesInMap = computed<{ code: string; count: number }[]>(() => {
  const counts: Record<string, number> = {}
  for (const p of projectsForCountryList.value) {
    if (!Array.isArray(p.country)) continue
    for (const code of p.country) {
      counts[code] = (counts[code] || 0) + 1
    }
  }
  return Object.entries(counts)
    .map(([code, count]) => ({ code, count }))
    .sort((a, b) =>
      (getCountryLabel(a.code) || a.code).localeCompare(getCountryLabel(b.code) || b.code)
    )
})

// Apply the search box on top of the active list. Selected countries
// always stay visible at the top so users can find them to deselect.
const visibleSidebarCountries = computed(() => {
  const q = countrySearch.value.trim().toLowerCase()
  const all = activeCountriesInMap.value
  if (!q) return all
  return all.filter((c) => {
    const label = (getCountryLabel(c.code) || '').toLowerCase()
    return label.includes(q) || c.code.toLowerCase().includes(q)
  })
})

const filteredProjects = computed(() => {
  let filtered = projects.value.filter((p) => !p.removedAt)

  const {
    searchQuery,
    selectedContinent,
    selectedCountries,
    selectedStatus,
    selectedRoles,
    selectedBizModels,
    selectedSizes,
    selectedGeoReach,
    selectedSectors,
    selectedResourceTypes
  } = filters.value

  if (searchQuery) {
    // Normalise: strip diacritics so "ceviche" matches "Céviche", "dudu" matches "Dûdû", etc.
    const normalize = (s: string) =>
      s
        .normalize('NFD')
        .replace(/[\u0300-\u036f]/g, '')
        .toLowerCase()

    const query = normalize(searchQuery)

    filtered = filtered.filter((p) => {
      const getSearchableText = (field: any): string => {
        if (!field) return ''
        if (typeof field === 'string') return normalize(field)
        if (typeof field === 'object') {
          return Object.values(field)
            .filter((v) => typeof v === 'string')
            .map((v) => normalize(v as string))
            .join(' ')
        }
        return ''
      }

      const searchableName = getSearchableText(p.name)
      const searchableDescription = getSearchableText(p.description)
      const searchableLocation = normalize(p.location || '')

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

  if (selectedRoles.length) {
    filtered = filtered.filter((p) =>
      p.entityRole?.some((r: string) => selectedRoles.includes(r))
    )
  }

  if (selectedBizModels.length) {
    filtered = filtered.filter((p) => p.bizModel && selectedBizModels.includes(p.bizModel))
  }

  if (selectedSizes.length) {
    filtered = filtered.filter((p) => p.entitySize && selectedSizes.includes(p.entitySize))
  }

  if (selectedGeoReach.length) {
    filtered = filtered.filter((p) => p.geoReach && selectedGeoReach.includes(p.geoReach))
  }

  if (selectedSectors.length) {
    filtered = filtered.filter((p) =>
      p.sectorFocus?.some((s: string) => selectedSectors.includes(s))
    )
  }

  if (selectedResourceTypes.length) {
    filtered = filtered.filter(
      (p) => p.resourceType && selectedResourceTypes.includes(p.resourceType)
    )
  }

  // Sort filtered projects
  const sorted = [...filtered].sort((a, b) => {
    let comparison = 0

    if (sortBy.value === 'score') {
      // "Random" — use the per-session shuffle order
      comparison = (shuffleIndex.value.get(a.pubId) ?? 0) - (shuffleIndex.value.get(b.pubId) ?? 0)
    } else if (sortBy.value === 'name') {
      const aName = typeof a.name === 'string' ? a.name : a.name?.en || ''
      const bName = typeof b.name === 'string' ? b.name : b.name?.en || ''
      comparison = aName.localeCompare(bName)
    } else if (sortBy.value === 'createdAt') {
      const aDate = a.createdAt ? a.createdAt * 1000 : 0
      const bDate = b.createdAt ? b.createdAt * 1000 : 0
      comparison = bDate - aDate
    }

    return sortOrder.value === 'asc' ? comparison : -comparison
  })

  return sorted
})

// Pagination
const totalPages = computed(() => Math.ceil(filteredProjects.value.length / itemsPerPage.value))

const paginatedProjects = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredProjects.value.slice(start, end)
})

// Mobile lazy loading
const displayedProjects = computed(() => {
  return filteredProjects.value.slice(0, mobileDisplayCount.value)
})

const hasMoreProjects = computed(() => {
  return mobileDisplayCount.value < filteredProjects.value.length
})

const loadMoreProjects = () => {
  mobileDisplayCount.value += 12
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

const goToPage = (page: number) => {
  currentPage.value = page
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Reset page when filters change
watch(
  filters,
  () => {
    currentPage.value = 1
  },
  { deep: true }
)

// Converts a project name to a URL slug
const slugify = (text: string) =>
  text
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 80)

// Build a full URL for a project (for right-click → open in new tab)
const getProjectUrl = (project: any) => {
  const name = typeof project.name === 'string' ? project.name : project.name?.en || ''
  const slug = slugify(name)
  return localePath(`/projects/${slug}`)
}

// Navigation handler
const handleProjectClick = (project: any, event?: MouseEvent) => {
  // Let middle-click and ctrl/cmd-click pass through to the browser
  if (event && (event.ctrlKey || event.metaKey || event.button === 1)) return
  event?.preventDefault()
  navigateTo(getProjectUrl(project))
}

// Reset all filters
const resetFilters = () => {
  filters.value = {
    searchQuery: '',
    selectedContinent: null,
    selectedCountries: [],
    selectedStatus: null,
    selectedRoles: [],
    selectedBizModels: [],
    selectedSizes: [],
    selectedGeoReach: [],
    selectedSectors: [],
    selectedResourceTypes: []
  }
  // Also clear URL query parameters and the saved selection
  router.push({ query: {} })
  try {
    localStorage.removeItem(FILTERS_STORAGE_KEY)
  } catch {
    // ignore
  }
}

// List view helpers
const { getLocalizedText } = useMultilingual()
const rowColors = ['#27421d', '#4ca049', '#5c4a2f', '#6b8e23', '#8b6f47']

const getRowName = (project: any) => {
  const name = project.name
  return typeof name === 'string' ? name : getLocalizedText(name, project.originalLang)
}

const getRowInitials = (project: any) => {
  const words = getRowName(project).trim().split(/\s+/)
  return words.length >= 2
    ? (words[0][0] + words[1][0]).toUpperCase()
    : getRowName(project).slice(0, 2).toUpperCase()
}

const getRowBackground = (project: any) => rowColors[project.pubId % rowColors.length]

const getRowDescription = (project: any) => {
  const desc = project.abstract || project.description
  if (!desc) return ''
  const text = typeof desc === 'string' ? desc : getLocalizedText(desc, project.originalLang)
  if (!text) return ''
  const firstLine = text.split(/[\n.]/)[0].trim()
  return firstLine.length > 120 ? firstLine.slice(0, 120) + '…' : firstLine
}

useHead({
  title: $t('nav.projects'),
  link: [{ rel: 'canonical', href: 'https://thesocioscope.org/projects/' }],
  meta: [
    {
      name: 'description',
      content:
        'Browse 700+ sustainable food system initiatives from around the world. Filter by country, theme, and sector to discover transformative projects documented by The Socioscope.'
    },
    { property: 'og:title', content: `${$t('nav.projects')} – The Socioscope` },
    {
      property: 'og:description',
      content:
        'Browse 700+ sustainable food system initiatives from around the world. Filter by country, theme, and sector to discover transformative projects documented by The Socioscope.'
    },
    { property: 'og:type', content: 'website' },
    { property: 'og:url', content: 'https://thesocioscope.org/projects/' },
    { property: 'og:site_name', content: 'The Socioscope' }
  ]
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/pagination' as *;
@use '~~/assets/styles/variables' as *;

.section {
  padding: 1.25rem 0 4rem; // tighter top because the title bar already gives breathing room
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

/* Clear all filters — only renders when any filter is active. */
.clear-all-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 0.4rem 0.75rem;
  background: white;
  border: 1px solid $border-strong;
  border-radius: 999px;
  color: $brown-dark;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  flex-shrink: 0;
  margin-top: 1rem;
  transition: border-color 0.15s, color 0.15s, background 0.15s;

  &:hover {
    border-color: $green-bright;
    color: $green-bright;
    background: rgba(76, 160, 73, 0.06);
  }

  &:focus-visible {
    outline: 2px solid $green-bright;
    outline-offset: 2px;
  }
}

.filters-bar {
  margin-bottom: 1.25rem;
}

.projects-map-wrap {
  margin-top: 1rem;
}

.map-layout {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr;

  @media (min-width: 1024px) {
    grid-template-columns: 320px 1fr;
  }
}

.map-sidebar {
  display: flex;
  flex-direction: column;
  background: white;
  border: 1px solid $border-soft;
  border-radius: 8px;
  overflow: hidden;
  max-height: calc(100vh - 240px);
  position: sticky;
  top: 1rem;
}

.sidebar-header {
  padding: 0.75rem 1rem;
  border-bottom: 1px solid $border-soft;
  background: $earth-10;
  font-size: 0.875rem;
  color: $text-caption;

  .sidebar-count strong {
    color: $green-dark;
    font-weight: 700;
  }
}

.sidebar-list {
  list-style: none;
  margin: 0;
  padding: 0;
  overflow-y: auto;
  flex: 1;
}

.sidebar-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.625rem 1rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: background 0.15s;

  &:hover {
    background: rgba(76, 160, 73, 0.06);
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: -2px;
  }
}

/* Country filter list — replaces the old paginated project list with
   a clickable, searchable country sidebar (OWID-style). */
.sidebar-search {
  position: relative;
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-bottom: 1px solid $border-soft;
  background: white;

  .search-icon {
    color: $text-caption;
    margin-right: 0.5rem;
    flex-shrink: 0;
  }
}

.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.875rem;
  font-family: inherit;
  color: $brown-dark;
  padding: 0.25rem 0;
  min-width: 0;

  &::placeholder {
    color: $text-disabled;
  }
}

.search-clear {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border: none;
  background: $earth-10;
  border-radius: 50%;
  color: $text-caption;
  cursor: pointer;
  flex-shrink: 0;

  &:hover {
    background: $earth-15;
    color: $brown-dark;
  }
}

.country-list {
  /* Override generic sidebar-list rules where needed */
}

.country-row {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  width: 100%;
  padding: 0.5rem 0.875rem;
  border: none;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
  background: transparent;
  text-align: left;
  cursor: pointer;
  transition: background 0.15s;
  font-family: inherit;
  font-size: 0.875rem;
  color: $brown-dark;

  &:hover {
    background: rgba(76, 160, 73, 0.06);
  }

  &.selected {
    background: rgba(76, 160, 73, 0.1);
    color: $green-dark;
    font-weight: 600;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: -2px;
  }
}

.country-checkbox {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 18px;
  height: 18px;
  border: 1.5px solid $border-strong;
  border-radius: 3px;
  background: white;
  flex-shrink: 0;
  color: white;
  transition: background 0.15s, border-color 0.15s;

  &.checked {
    background: $green-bright;
    border-color: $green-bright;
  }

  &:hover {
    border-color: $green-bright;
  }
}

.country-name {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.country-empty {
  padding: 1rem 0.875rem;
  font-size: 0.875rem;
  color: $text-caption;
  text-align: center;
}

.sidebar-actions {
  padding: 0.5rem 0.75rem;
  border-top: 1px solid $border-soft;
  background: $earth-10;
}

.reset-countries {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  width: 100%;
  justify-content: center;
  padding: 0.4rem 0.5rem;
  background: white;
  border: 1px solid $border-strong;
  border-radius: 4px;
  color: $brown-dark;
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.15s, color 0.15s;

  &:hover {
    border-color: $green-bright;
    color: $green-bright;
  }
}

.sidebar-row-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.sidebar-row-body {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  flex: 1;
}

.sidebar-row-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: $brown-dark;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sidebar-row-meta {
  font-size: 0.75rem;
  color: $text-caption;
  display: flex;
  align-items: center;
  gap: 2px;
}

.sidebar-pagination {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  border-top: 1px solid $border-soft;
  background: $earth-10;

  .page-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    border: 1px solid $border-strong;
    background: white;
    border-radius: 4px;
    color: $text-caption;
    cursor: pointer;

    &:disabled {
      opacity: 0.4;
      cursor: not-allowed;
    }

    &:hover:not(:disabled) {
      color: $green-dark;
      border-color: $green-bright;
    }

    &:focus-visible {
      outline: 2px solid $green-dark;
      outline-offset: 2px;
    }
  }

  .page-info {
    font-size: 0.8125rem;
    color: $text-caption;
  }
}

.map-area {
  min-width: 0;
}

.map-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 320px;
  background: white;
  border: 1px solid $border-soft;
  border-radius: 8px;
}

// Toolbar row: ListControls (sort) + view toggle as a segmented control
.toolbar-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 1.25rem;
}

.view-toggle.segmented {
  display: inline-flex;
  border: 1px solid $border-strong;
  border-radius: 8px;
  overflow: hidden;
  flex-shrink: 0;
  background: white;

  @media (max-width: 600px) {
    width: 100%;
  }
}

.view-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: white;
  border: none;
  padding: 8px 14px;
  cursor: pointer;
  color: $text-caption;
  font-size: 0.875rem;
  font-weight: 500;
  transition: background 0.15s, color 0.15s;

  & + .view-btn {
    border-left: 1px solid $border-soft;
  }

  .btn-label {
    @media (max-width: 600px) {
      // On phones we keep the label since the segmented control fills width
      display: inline;
    }
  }

  &:hover:not(.active) {
    background: $earth-10;
    color: $text-primary;
  }

  &.active {
    background: $green-bright;
    color: white;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: -2px;
    z-index: 1;
  }

  @media (max-width: 600px) {
    flex: 1;
    justify-content: center;
  }
}

.projects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin: 2rem 0;

  /* Mobile: single column with comfortable row gap. The horizontal
     cards are tall enough to read at a glance (~140px each) while
     still fitting 3 per screen on a typical phone viewport. */
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 0.875rem;
    margin: 1rem 0;
  }

  /* CRITICAL: grid items default to `min-width: auto` which lets them
     grow to their intrinsic content width. The card's horizontal scroll
     strip has 4 panels × 100% width each — that "intrinsic width" is
     ~4× the viewport, so the card overflows the right edge. min-width: 0
     forces the grid item to respect the column track instead. */
  > * {
    min-width: 0;
    max-width: 100%;
  }
}

.projects-list {
  margin: 2rem 0;
  border: 1px solid #e5e5e5;
  border-radius: 4px;
  overflow: hidden;
}

.project-row {
  display: flex;
  align-items: center;
  gap: 1.25rem;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f0f0f0;
  cursor: pointer;
  transition: background 0.2s;
  text-decoration: none;
  color: inherit;

  &:last-child {
    border-bottom: none;
  }

  &:hover {
    background: #fafafa;
  }
}

.row-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.row-body {
  flex: 1;
  min-width: 0;
}

.row-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: $brown-dark;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 0.2rem;
}

.row-location {
  font-size: 0.8rem;
  color: #888;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 2px;
}

.row-description {
  font-size: 0.8rem;
  color: #888;
  margin: 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.row-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  flex-shrink: 0;

  @media (max-width: 600px) {
    display: none;
  }
}

.row-arrow {
  color: #ccc;
  flex-shrink: 0;
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
</style>
