<template>
  <!-- Stacked layout (used inside the mobile dialog) — plain vertical stack. -->
  <div v-if="stacked" class="fields-stacked">
    <v-select
      v-if="!excludeContinent"
      :model-value="filters.selectedContinent"
      :items="continentOptions"
      :label="$t('projects.filterByContinent', 'Filter by continent')"
      clearable
      outlined
      bg-color="white"
      hide-details
      density="comfortable"
      @update:model-value="emit('update', 'selectedContinent', $event)"
    />
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
      @update:model-value="emit('update', 'selectedCountries', $event)"
    />
    <v-autocomplete
      :model-value="filters.selectedRoles"
      :items="roleOptions"
      :label="$t('projects.filterByRole', 'Filter by entity role')"
      multiple
      chips
      closable-chips
      clearable
      outlined
      bg-color="white"
      hide-details
      density="comfortable"
      @update:model-value="emit('update', 'selectedRoles', $event)"
    />
    <v-autocomplete
      :model-value="filters.selectedBizModels"
      :items="bizModelOptions"
      :label="$t('projects.filterByBizModel', 'Filter by business model')"
      multiple
      chips
      closable-chips
      clearable
      outlined
      bg-color="white"
      hide-details
      density="comfortable"
      @update:model-value="emit('update', 'selectedBizModels', $event)"
    />
    <v-autocomplete
      :model-value="filters.selectedSizes"
      :items="sizeOptions"
      :label="$t('projects.filterBySize', 'Filter by size')"
      multiple
      chips
      closable-chips
      clearable
      outlined
      bg-color="white"
      hide-details
      density="comfortable"
      @update:model-value="emit('update', 'selectedSizes', $event)"
    />
    <v-autocomplete
      :model-value="filters.selectedGeoReach"
      :items="geoReachOptions"
      :label="$t('projects.filterByGeoReach', 'Filter by geographic reach')"
      multiple
      chips
      closable-chips
      clearable
      outlined
      bg-color="white"
      hide-details
      density="comfortable"
      @update:model-value="emit('update', 'selectedGeoReach', $event)"
    />
    <v-autocomplete
      :model-value="filters.selectedSectors"
      :items="sectorOptions"
      :label="$t('projects.filterBySector', 'Filter by sector focus')"
      multiple
      chips
      closable-chips
      clearable
      outlined
      bg-color="white"
      hide-details
      density="comfortable"
      @update:model-value="emit('update', 'selectedSectors', $event)"
    />
    <v-autocomplete
      :model-value="filters.selectedResourceTypes"
      :items="resourceTypeOptions"
      :label="$t('projects.filterByResource', 'Filter by resource type')"
      multiple
      chips
      closable-chips
      clearable
      outlined
      bg-color="white"
      hide-details
      density="comfortable"
      @update:model-value="emit('update', 'selectedResourceTypes', $event)"
    />
  </div>

  <!-- Inline grid (desktop / tablet) — Vuetify 3×3 layout. -->
  <v-row v-else>
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
        @update:model-value="emit('update', 'selectedContinent', $event)"
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
        @update:model-value="emit('update', 'selectedCountries', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedRoles"
        :items="roleOptions"
        :label="$t('projects.filterByRole', 'Filter by entity role')"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="emit('update', 'selectedRoles', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedBizModels"
        :items="bizModelOptions"
        :label="$t('projects.filterByBizModel', 'Filter by business model')"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="emit('update', 'selectedBizModels', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedSizes"
        :items="sizeOptions"
        :label="$t('projects.filterBySize', 'Filter by size')"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="emit('update', 'selectedSizes', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedGeoReach"
        :items="geoReachOptions"
        :label="$t('projects.filterByGeoReach', 'Filter by geographic reach')"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="emit('update', 'selectedGeoReach', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedSectors"
        :items="sectorOptions"
        :label="$t('projects.filterBySector', 'Filter by sector focus')"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="emit('update', 'selectedSectors', $event)"
      />
    </v-col>
    <v-col cols="12" sm="6" md="4">
      <v-autocomplete
        :model-value="filters.selectedResourceTypes"
        :items="resourceTypeOptions"
        :label="$t('projects.filterByResource', 'Filter by resource type')"
        multiple
        chips
        closable-chips
        clearable
        outlined
        bg-color="white"
        hide-details
        density="comfortable"
        @update:model-value="emit('update', 'selectedResourceTypes', $event)"
      />
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

defineProps<{
  filters: FilterValues
  continentOptions: SelectOption[]
  countryOptions: SelectOption[]
  roleOptions: string[]
  bizModelOptions: string[]
  sizeOptions: string[]
  geoReachOptions: string[]
  sectorOptions: string[]
  resourceTypeOptions: string[]
  stacked?: boolean
  excludeContinent?: boolean
}>()

const emit = defineEmits<{
  update: [key: keyof FilterValues, value: string | string[] | null]
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.fields-stacked {
  display: flex;
  flex-direction: column;
  gap: $rhythm-2;
}
</style>
