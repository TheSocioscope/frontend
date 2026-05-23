<template>
  <div class="projects-filters">
    <!-- Search row: always visible. Mobile: + Filters button stacked underneath. -->
    <div class="filters-top">
      <v-text-field
        :model-value="filters.searchQuery"
        :label="$t('projects.search', 'Search projects')"
        prepend-inner-icon="mdi-magnify"
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        class="filters-search"
        @update:model-value="updateFilter('searchQuery', $event)"
      />

      <!-- Mobile-only: prominent "Customize" button (OWID pattern) opens
           the dialog with every filter. -->
      <v-btn
        class="filters-trigger filters-trigger-mobile"
        variant="flat"
        color="primary"
        size="large"
        prepend-icon="mdi-tune-variant"
        block
        @click="filterDialogOpen = true"
      >
        {{ $t('projects.customizeSearch', 'Customize search') }}
        <span v-if="totalActiveCount > 0" class="filters-badge filters-badge-on-primary">
          {{ totalActiveCount }}
        </span>
      </v-btn>
    </div>

    <!-- OWID-style horizontal compact filter row (desktop only) -->
    <div class="filters-bar-desktop" role="group" :aria-label="$t('projects.filters', 'Filters')">
      <div class="filter-cell">
        <span class="filter-label">{{ $t('projects.continent', 'Continent') }}</span>
        <v-select
          :model-value="filters.selectedContinent"
          :items="continentOptions"
          :placeholder="$t('common.all', 'All')"
          clearable
          density="compact"
          hide-details
          variant="outlined"
          bg-color="white"
          @update:model-value="updateFilter('selectedContinent', $event)"
        />
      </div>
      <div class="filter-cell">
        <span class="filter-label">{{ $t('projects.sector', 'Sector') }}</span>
        <v-autocomplete
          :model-value="filters.selectedSectors"
          :items="sectorOptions"
          :placeholder="$t('common.all', 'All')"
          multiple
          chips
          closable-chips
          clearable
          density="compact"
          hide-details
          variant="outlined"
          bg-color="white"
          @update:model-value="updateFilter('selectedSectors', $event)"
        />
      </div>
      <div class="filter-cell">
        <span class="filter-label">{{ $t('projects.country', 'Country') }}</span>
        <v-autocomplete
          :model-value="filters.selectedCountries"
          :items="countryOptions"
          :placeholder="$t('common.all', 'All')"
          multiple
          chips
          closable-chips
          clearable
          density="compact"
          hide-details
          variant="outlined"
          bg-color="white"
          @update:model-value="updateFilter('selectedCountries', $event)"
        />
      </div>
      <div class="filter-cell">
        <span class="filter-label">{{ $t('projects.role', 'Role') }}</span>
        <v-autocomplete
          :model-value="filters.selectedRoles"
          :items="roleOptions"
          :placeholder="$t('common.all', 'All')"
          multiple
          chips
          closable-chips
          clearable
          density="compact"
          hide-details
          variant="outlined"
          bg-color="white"
          @update:model-value="updateFilter('selectedRoles', $event)"
        />
      </div>
      <button
        type="button"
        class="filters-trigger-desktop"
        @click="filterDialogOpen = true"
      >
        <v-icon size="small">mdi-tune-variant</v-icon>
        <span>{{ $t('projects.moreFilters', 'More filters') }}</span>
        <span v-if="dialogExtraActiveCount > 0" class="filters-badge">
          {{ dialogExtraActiveCount }}
        </span>
      </button>

      <button
        v-if="hasActiveFilters"
        type="button"
        class="filters-clear-inline"
        @click="resetAllFilters"
      >
        <v-icon size="small">mdi-close-circle</v-icon>
        {{ $t('common.resetFilters') }}
      </button>
    </div>

    <!-- Non-modal bottom sheet (OWID Customize pattern). Slides up from
         the bottom but only takes ~60vh; the page above stays scrollable
         and interactive. The sheet stays anchored as the user scrolls. -->
    <Teleport to="body">
      <Transition name="customize-sheet">
        <aside
          v-if="filterDialogOpen"
          class="customize-sheet"
          role="dialog"
          aria-modal="false"
          :aria-label="$t('projects.filters', 'Filters')"
        >
          <header class="sheet-header">
            <h2 class="sheet-title">{{ $t('projects.filters', 'Filters') }}</h2>
            <button
              type="button"
              class="sheet-close"
              :aria-label="$t('common.close', 'Close')"
              @click="filterDialogOpen = false"
            >
              <v-icon>mdi-close</v-icon>
            </button>
          </header>

          <div class="sheet-body">
            <!-- Sort controls live in the sheet on mobile (OWID pattern). -->
            <div v-if="sortOptions && sortOptions.length" class="sheet-sort">
              <span class="sheet-section-label">{{ $t('projects.sortBy', 'Sort by') }}</span>
              <div class="sheet-sort-row">
                <v-select
                  :model-value="sortBy"
                  :items="sortOptions"
                  item-title="label"
                  item-value="value"
                  density="compact"
                  hide-details
                  variant="outlined"
                  bg-color="white"
                  class="sheet-sort-select"
                  @update:model-value="emit('update:sortBy', $event)"
                />
                <button
                  type="button"
                  class="sheet-sort-toggle"
                  :aria-label="
                    sortOrder === 'asc'
                      ? $t('projects.sortDescending', 'Sort descending')
                      : $t('projects.sortAscending', 'Sort ascending')
                  "
                  @click="emit('update:sortOrder', sortOrder === 'asc' ? 'desc' : 'asc')"
                >
                  <v-icon>{{ sortOrder === 'asc' ? 'mdi-arrow-up' : 'mdi-arrow-down' }}</v-icon>
                </button>
              </div>
            </div>

            <ProjectsFilterFields
              :filters="filters"
              :continent-options="continentOptions"
              :country-options="countryOptions"
              :role-options="roleOptions"
              :biz-model-options="bizModelOptions"
              :size-options="sizeOptions"
              :geo-reach-options="geoReachOptions"
              :sector-options="sectorOptions"
              :resource-type-options="resourceTypeOptions"
              stacked
              @update="updateFilter"
            />
          </div>

          <footer class="sheet-footer">
            <button
              type="button"
              class="sheet-reset"
              :disabled="!hasActiveFilters"
              @click="resetAllFilters"
            >
              {{ $t('common.resetFilters') }}
            </button>
            <button
              type="button"
              class="sheet-done"
              @click="filterDialogOpen = false"
            >
              {{ $t('common.done', 'Done') }}
              <span v-if="dialogActiveCount > 0">&nbsp;({{ dialogActiveCount }})</span>
            </button>
          </footer>
        </aside>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
interface FilterValues {
  searchQuery: string
  selectedContinent: string | null
  selectedCountries: string[]
  selectedStatus: string | null
  selectedRoles: string[]
  selectedBizModels: string[]
  selectedSizes: string[]
  selectedGeoReach: string[]
  selectedSectors: string[]
  selectedResourceTypes: string[]
}

interface SelectOption {
  value: string
  title: string
}

interface SortOption {
  value: string
  label: string
}

interface Props {
  filters: FilterValues
  continentOptions: SelectOption[]
  countryOptions: SelectOption[]
  statusOptions: SelectOption[]
  roleOptions: string[]
  bizModelOptions: string[]
  sizeOptions: string[]
  geoReachOptions: string[]
  sectorOptions: string[]
  resourceTypeOptions: string[]
  // Sort props (optional) — when present, the Customize sheet renders a
  // sort section so mobile users don't need a separate toolbar row.
  sortBy?: string
  sortOrder?: 'asc' | 'desc'
  sortOptions?: SortOption[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [filters: FilterValues]
  'update:sortBy': [value: string]
  'update:sortOrder': [value: 'asc' | 'desc']
  reset: []
}>()

const { t: $t } = useI18n()

const filterDialogOpen = ref(false)

// Toggle a body class so the page can reserve scroll space below the sheet —
// otherwise the last cards/pagination get hidden behind the fixed sheet.
watch(filterDialogOpen, (open) => {
  if (typeof document === 'undefined') return
  document.body.classList.toggle('has-customize-sheet-open', open)
})

onBeforeUnmount(() => {
  if (typeof document === 'undefined') return
  document.body.classList.remove('has-customize-sheet-open')
})

const updateFilter = (key: keyof FilterValues, value: string | string[] | null) => {
  emit('update:modelValue', { ...props.filters, [key]: value })
}

const hasActiveFilters = computed(() => {
  const f = props.filters
  return !!(
    f.searchQuery ||
    f.selectedContinent ||
    f.selectedCountries.length > 0 ||
    f.selectedStatus ||
    f.selectedRoles.length > 0 ||
    f.selectedBizModels.length > 0 ||
    f.selectedSizes.length > 0 ||
    f.selectedGeoReach.length > 0 ||
    f.selectedSectors.length > 0 ||
    f.selectedResourceTypes.length > 0
  )
})

// Mobile dialog badge: counts everything except inline-Continent.
const dialogActiveCount = computed(() => {
  const f = props.filters
  return (
    f.selectedCountries.length +
    (f.selectedStatus ? 1 : 0) +
    f.selectedRoles.length +
    f.selectedBizModels.length +
    f.selectedSizes.length +
    f.selectedGeoReach.length +
    f.selectedSectors.length +
    f.selectedResourceTypes.length
  )
})

// Desktop "More filters" badge: counts only filters not in the inline desktop
// row (i.e., not Continent, Sector, Country, or Role).
const dialogExtraActiveCount = computed(() => {
  const f = props.filters
  return (
    (f.selectedStatus ? 1 : 0) +
    f.selectedBizModels.length +
    f.selectedSizes.length +
    f.selectedGeoReach.length +
    f.selectedResourceTypes.length
  )
})

// "Reset filters (n)" reflects every active filter, including the inline
// Continent — that's the user's mental model for "clear all."
const totalActiveCount = computed(() => {
  return dialogActiveCount.value + (props.filters.selectedContinent ? 1 : 0)
})

const resetAllFilters = () => {
  emit('reset')
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.projects-filters {
  width: 100%;
}

.filters-top {
  display: flex;
  align-items: stretch;
  gap: $rhythm-2;
  margin-bottom: $rhythm-2;

  .filters-search {
    flex: 1;
    min-width: 0;
  }

  .filters-trigger-mobile {
    flex-shrink: 0;
    position: relative;
    display: none;
  }
}

@media (max-width: $detail-bp-tablet - 1) {
  .filters-top {
    flex-direction: column;
    align-items: stretch;
    gap: $rhythm-1;
  }

  .filters-top .filters-trigger-mobile {
    display: inline-flex;
    width: 100%;
    justify-content: center;
  }
}

// OWID-style horizontal compact filter row (desktop)
.filters-bar-desktop {
  display: grid;
  grid-template-columns: repeat(4, minmax(140px, 1fr)) auto auto;
  gap: $rhythm-2;
  align-items: end;
  padding: $rhythm-2;
  background: $earth-10;
  border: 1px solid $border-soft;
  border-radius: 8px;
  margin-bottom: $rhythm-3;

  @media (max-width: $detail-bp-desktop - 1) {
    // Two-column layout on tablet
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: $detail-bp-tablet - 1) {
    display: none;
  }
}

.filter-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
}

.filter-label {
  font-size: 10px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: $text-caption;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.filters-trigger-desktop {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: white;
  border: 1px solid $border-strong;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.78);
  white-space: nowrap;
  align-self: end;
  height: 40px;

  &:hover {
    border-color: $green-bright;
    color: $green-dark;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
  }
}

.filters-clear-inline {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 0.875rem;
  color: $text-caption;
  text-decoration: underline;
  align-self: end;
  padding: 6px 0;
  height: 40px;

  &:hover {
    color: $green-dark;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
    border-radius: 2px;
  }
}

.filters-badge {
  margin-left: 6px;
  background: $green-bright;
  color: white;
  border-radius: 999px;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 700;
  line-height: 1.1;
  min-width: 22px;
  text-align: center;

  &.filters-badge-on-primary {
    background: white;
    color: $green-dark;
  }
}


/* ============================================================
   Customize bottom sheet — non-modal, partial-height, stays
   anchored to the viewport bottom while the page scrolls above.
   Mirrors the OWID Conflict-Data-Explorer Customize pattern.
   ============================================================ */
.customize-sheet {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 60;
  display: flex;
  flex-direction: column;

  /* Cap height so the page above stays visible/interactive */
  max-height: 60vh;
  height: 60vh;

  background: $surface-card;
  border-top: 1px solid $border-strong;
  border-top-left-radius: 12px;
  border-top-right-radius: 12px;
  box-shadow: 0 -8px 24px rgba(0, 0, 0, 0.12);

  /* Allow keyboard / dropdown popovers inside the sheet to overlay
     beyond its bottom edge (Vuetify v-select menus open above) */
  overflow: visible;

  /* Tablet/desktop: cap width and centre — the sheet remains a pill at
     the page bottom so the existing inline filter strip on desktop is
     unobstructed. */
  @media (min-width: 768px) {
    max-width: 720px;
    left: 50%;
    transform: translateX(-50%);
    border-radius: 12px 12px 0 0;
  }
}

/* Slide-up transition (skipped under reduced-motion via global media) */
.customize-sheet-enter-active,
.customize-sheet-leave-active {
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.customize-sheet-enter-from,
.customize-sheet-leave-to {
  transform: translateY(100%);
  opacity: 0;

  @media (min-width: 768px) {
    /* Compose with the centring translateX above */
    transform: translate(-50%, 100%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .customize-sheet-enter-active,
  .customize-sheet-leave-active {
    transition: none;
  }
}

.sheet-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: $spacing-md $spacing-lg;
  border-bottom: 1px solid $border-soft;
  flex-shrink: 0;
}

.sheet-title {
  margin: 0;
  font-family: $font-family-display;
  font-size: 1.125rem;
  font-weight: 700;
  color: $green-forest;
}

.sheet-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 50%;
  color: $green-leaf;
  cursor: pointer;
  transition: background 0.15s, color 0.15s;

  &:hover {
    background: $earth-10;
    color: $green-forest;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }
}

.sheet-body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: $spacing-md $spacing-lg;
  background: $surface-page;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;

  /* Smooth iOS momentum scrolling */
  -webkit-overflow-scrolling: touch;
}

.sheet-section-label {
  display: block;
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: $text-caption;
  margin-bottom: 6px;
}

.sheet-sort-row {
  display: flex;
  align-items: stretch;
  gap: $spacing-xs;
}

.sheet-sort-select {
  flex: 1;
  min-width: 0;
}

.sheet-sort-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: $green-leaf;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  flex-shrink: 0;
  transition: background 0.15s;

  &:hover {
    background: $green-leaf-dark;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }
}

.sheet-footer {
  display: flex;
  align-items: center;
  gap: $spacing-md;
  padding: $spacing-sm $spacing-lg;
  border-top: 1px solid $border-soft;
  background: $surface-card;
  flex-shrink: 0;
}

.sheet-reset {
  background: transparent;
  border: none;
  padding: 8px 4px;
  font: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  color: $text-secondary;
  cursor: pointer;
  text-transform: uppercase;
  letter-spacing: 0.05em;

  &:disabled {
    color: $text-disabled;
    cursor: not-allowed;
  }

  &:not(:disabled):hover {
    color: $green-forest;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
    border-radius: 2px;
  }
}

.sheet-done {
  margin-left: auto;
  background: $green-leaf;
  color: white;
  border: none;
  padding: 10px 28px;
  border-radius: 4px;
  font: inherit;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;

  &:hover {
    background: $green-leaf-dark;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }
}
</style>
