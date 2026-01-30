<template>
  <div class="controls">
    <div class="sort-controls">
      <label>{{ sortLabel }}:</label>
      <select v-model="internalSortBy" class="select">
        <option v-for="option in sortOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
      <button class="sort-btn" @click="toggleSort">
        {{ internalSortOrder === 'asc' ? '▲' : '▼' }}
      </button>
    </div>

    <div v-if="showPerPage" class="per-page-controls">
      <label>{{ perPageLabel }}:</label>
      <select v-model.number="internalItemsPerPage" class="select">
        <option v-for="option in perPageOptions" :key="option" :value="option">
          {{ option }}
        </option>
      </select>
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
</style>
