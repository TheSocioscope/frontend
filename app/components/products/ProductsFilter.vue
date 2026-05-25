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

/* Compact pill row — sleeker than the big block buttons. Centered on
   desktop; on mobile it scrolls horizontally so the row stays one line. */
.filter-section {
  margin: 0 auto 1.25rem;
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  flex-wrap: wrap;

  @media (max-width: 600px) {
    flex-wrap: nowrap;
    overflow-x: auto;
    justify-content: flex-start;
    padding-bottom: 0.25rem;
    scrollbar-width: none;

    &::-webkit-scrollbar {
      display: none;
    }
  }
}

.filter-btn {
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid $cream-dark;
  border-radius: 999px;
  color: $brown-dark;
  font-family: $font-family-display;
  font-size: 0.875rem;
  font-weight: $font-weight-semibold;
  cursor: pointer;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;
  white-space: nowrap;
  flex-shrink: 0;

  &:hover {
    border-color: $green-bright;
    color: $green-bright;
  }

  &.active {
    background: $green-bright;
    color: white;
    border-color: $green-bright;
  }

  &:focus-visible {
    outline: 2px solid $green-bright;
    outline-offset: 2px;
  }
}
</style>
