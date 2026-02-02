<template>
  <div class="controls">
    <div class="sort-controls">
      <label>{{ sortLabel }}:</label>
      <v-select
        v-model="internalSortBy"
        :items="sortOptions"
        item-title="label"
        item-value="value"
        variant="outlined"
        bg-color="white"
        rounded="0"
        hide-details
        density="compact"
        class="sort-select"
      />
      <v-btn variant="outlined" rounded="0" height="40" class="sort-btn" @click="toggleSort">
        <v-icon color="white">{{
          internalSortOrder === 'asc' ? 'mdi-arrow-up' : 'mdi-arrow-down'
        }}</v-icon>
      </v-btn>
    </div>

    <slot name="center" />

    <div v-if="showPerPage" class="per-page-controls">
      <label>{{ perPageLabel }}:</label>
      <v-select
        v-model.number="internalItemsPerPage"
        :items="perPageOptions"
        variant="outlined"
        bg-color="white"
        rounded="0"
        hide-details
        density="compact"
        class="per-page-select"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface SortOption {
  value: string
  label: string
}

interface Props {
  sortBy: string
  sortOrder: 'asc' | 'desc'
  itemsPerPage?: number
  sortOptions: SortOption[]
  perPageOptions?: number[]
  sortLabel?: string
  perPageLabel?: string
  showPerPage?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  itemsPerPage: 20,
  perPageOptions: () => [10, 20, 50, 100],
  sortLabel: 'Sort by',
  perPageLabel: 'Items per page',
  showPerPage: true
})

const emit = defineEmits<{
  'update:sortBy': [value: string]
  'update:sortOrder': [value: 'asc' | 'desc']
  'update:itemsPerPage': [value: number]
}>()

const internalSortBy = computed({
  get: () => props.sortBy,
  set: (value) => emit('update:sortBy', value)
})

const internalSortOrder = computed({
  get: () => props.sortOrder,
  set: (value) => emit('update:sortOrder', value)
})

const internalItemsPerPage = computed({
  get: () => props.itemsPerPage,
  set: (value) => emit('update:itemsPerPage', value)
})

const toggleSort = () => {
  internalSortOrder.value = internalSortOrder.value === 'asc' ? 'desc' : 'asc'
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/pagination' as *;

.sort-btn {
  min-width: 40px !important;
  width: 40px;
  background-color: rgb(var(--v-theme-primary)) !important;
}
</style>
