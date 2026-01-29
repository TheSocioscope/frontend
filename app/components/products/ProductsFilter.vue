<template>
  <div class="filter-section">
    <button
      v-for="filter in filters"
      :key="filter.value"
      class="filter-btn"
      :class="{ active: activeFilter === filter.value }"
      @click="$emit('filter-change', filter.value)"
    >
      {{ $t(filter.label) }}
    </button>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

defineProps<{
  activeFilter: string
}>()

defineEmits<{
  'filter-change': [value: string]
}>()

const filters = [
  { value: 'all', label: 'products.filters.all' },
  { value: 'food', label: 'products.filters.food' },
  { value: 'tools', label: 'products.filters.tools' },
  { value: 'services', label: 'products.filters.services' },
  { value: 'education', label: 'products.filters.education' }
]
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.filter-section {
  max-width: 800px;
  margin: 0 auto 3rem;
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.filter-btn {
  padding: 0.75rem 1.75rem;
  background: white;
  border: 2px solid $warm-beige;
  color: $brown-dark;
  font-family: $font-family-display;
  font-size: 1rem;
  font-weight: $font-weight-semibold;
  cursor: pointer;
  transition: all 0.3s ease;

  &:hover,
  &.active {
    background: $green-bright;
    color: white;
    border-color: $green-bright;
  }
}
</style>
