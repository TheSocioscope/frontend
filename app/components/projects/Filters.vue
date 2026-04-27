<template>
  <v-row>
    <!-- Row 1: Search / Continent / Countries -->
    <v-col cols="12" md="4">
      <v-text-field
        :model-value="filters.searchQuery"
        :label="$t('projects.search', 'Search projects')"
        prepend-inner-icon="mdi-magnify"
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('searchQuery', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-select
        :model-value="filters.selectedContinent"
        :items="continentOptions"
        :label="$t('projects.filterByContinent', 'Filter by continent')"
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedContinent', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedCountries"
        :items="countryOptions"
        :label="$t('projects.filterByCountry', 'Filter by country')"
        multiple
        chips
        closable-chips
        outlined
        bg-color="white"
        clearable
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedCountries', $event)"
      />
    </v-col>

    <!-- Row 2: Entity Role / Business Model / Size -->
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedRoles"
        :items="roleOptions"
        label="Filter by entity role"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedRoles', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedBizModels"
        :items="bizModelOptions"
        label="Filter by business model"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedBizModels', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedSizes"
        :items="sizeOptions"
        label="Filter by size"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedSizes', $event)"
      />
    </v-col>

    <!-- Row 3: Geographic Reach / Sector Focus / Resource Type -->
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedGeoReach"
        :items="geoReachOptions"
        label="Filter by geographic reach"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedGeoReach', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedSectors"
        :items="sectorOptions"
        label="Filter by sector focus"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedSectors', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedResourceTypes"
        :items="resourceTypeOptions"
        label="Filter by resource type"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedResourceTypes', $event)"
      />
    </v-col>
  </v-row>

  <!-- Filter Reset Button Row -->
  <v-row v-if="hasActiveFilters" class="mt-2">
    <v-col cols="12" class="d-flex justify-center">
      <ListFilterResetButton :has-active-filters="hasActiveFilters" @reset="resetAllFilters" />
    </v-col>
  </v-row>
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
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [filters: FilterValues]
  reset: []
}>()

const { t: $t } = useI18n()

const updateFilter = (key: keyof FilterValues, value: string | string[] | null) => {
  emit('update:modelValue', { ...props.filters, [key]: value })
}

const hasActiveFilters = computed(() => {
  return !!(
    props.filters.searchQuery ||
    props.filters.selectedContinent ||
    props.filters.selectedCountries.length > 0 ||
    props.filters.selectedStatus ||
    props.filters.selectedRoles.length > 0 ||
    props.filters.selectedBizModels.length > 0 ||
    props.filters.selectedSizes.length > 0 ||
    props.filters.selectedGeoReach.length > 0 ||
    props.filters.selectedSectors.length > 0 ||
    props.filters.selectedResourceTypes.length > 0
  )
})

const resetAllFilters = () => {
  emit('reset')
}
</script>
