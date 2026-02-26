<template>
  <v-row>
    <!-- Row 1 -->
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

    <!-- Row 2 -->
    <v-col cols="12" sm="6" md="3">
      <v-autocomplete
        :model-value="filters.selectedThematics"
        :items="thematicOptions"
        :label="$t('projects.filterByThematic', 'Filter by thematics')"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedThematics', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="3">
      <v-autocomplete
        :model-value="filters.selectedFields"
        :items="fieldOptions"
        :label="$t('projects.filterByField', 'Filter by fields')"
        multiple
        chips
        outlined
        bg-color="white"
        closable-chips
        clearable
        hide-details
        density="comfortable"
        @update:model-value="updateFilter('selectedFields', $event)"
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
  selectedThematics: string[]
  selectedFields: string[]
  selectedTypes: string[]
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
  thematicOptions: SelectOption[]
  fieldOptions: SelectOption[]
  typeOptions: SelectOption[]
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

// Check if any filters are active
const hasActiveFilters = computed(() => {
  return !!(
    props.filters.searchQuery ||
    props.filters.selectedContinent ||
    props.filters.selectedCountries.length > 0 ||
    props.filters.selectedStatus ||
    props.filters.selectedThematics.length > 0 ||
    props.filters.selectedFields.length > 0 ||
    props.filters.selectedTypes.length > 0
  )
})

const resetAllFilters = () => {
  emit('reset')
}
</script>
