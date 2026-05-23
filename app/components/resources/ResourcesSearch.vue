<template>
  <div class="search-filter-section">
    <div class="search-bar">
      <v-icon class="search-icon" size="small">mdi-magnify</v-icon>
      <input
        v-model="localSearch"
        type="text"
        class="search-input"
        :placeholder="$t('resources.search.placeholder')"
        @input="handleSearch"
      />
      <button
        v-if="localSearch"
        type="button"
        class="search-clear"
        :aria-label="$t('common.clear', 'Clear')"
        @click="clearSearch"
      >
        <v-icon size="x-small">mdi-close</v-icon>
      </button>
    </div>
    <div class="filter-buttons">
      <button
        v-for="filter in filters"
        :key="filter.value"
        class="filter-btn"
        :class="{ active: activeFilter === filter.value }"
        @click="handleFilterChange(filter.value)"
      >
        {{ filter.label }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

const props = defineProps<{
  activeFilter: string
  searchQuery: string
}>()

const emit = defineEmits<{
  'filter-change': [value: string]
  'search-change': [value: string]
}>()

const localSearch = ref(props.searchQuery)

// Watch for prop changes to sync local state
watch(
  () => props.searchQuery,
  (newValue) => {
    localSearch.value = newValue
  }
)

const filters = computed(() => [
  { value: 'all', label: t('resources.filters.all') },
  { value: 'article', label: t('resources.filters.article') },
  { value: 'book', label: t('resources.filters.book') },
  { value: 'event', label: t('resources.filters.event') },
  { value: 'funding', label: t('resources.filters.funding') },
  { value: 'organization', label: t('resources.filters.organization') },
  { value: 'policy', label: t('resources.filters.policy') },
  { value: 'socioscope', label: t('resources.filters.socioscope') }
])

const handleFilterChange = (value: string) => {
  emit('filter-change', value)
}

const handleSearch = () => {
  emit('search-change', localSearch.value)
}

const clearSearch = () => {
  localSearch.value = ''
  emit('search-change', '')
}
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.search-filter-section {
  margin-bottom: 1.25rem;
}

.search-bar {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  border: 1px solid $border-cream;
  border-radius: 8px;
  padding: 0 0.875rem;
  margin-bottom: 0.875rem;
  transition: border-color 0.2s ease;

  &:focus-within {
    border-color: $green-bright;
  }
}

.search-icon {
  color: $text-caption;
  flex-shrink: 0;
}

.search-input {
  flex: 1;
  padding: 0.625rem 0;
  border: none;
  outline: none;
  background: transparent;
  font-size: 0.9375rem;
  font-family: inherit;
  color: $brown-dark;
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

/* Compact pill row — sleeker than the big block buttons. Mobile makes
   this a horizontal scroll strip so the row stays one line. */
.filter-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
  justify-content: center;

  @media (max-width: 600px) {
    flex-wrap: nowrap;
    overflow-x: auto;
    justify-content: flex-start;
    padding-bottom: 0.25rem;
    margin: 0 -1rem;
    padding-left: 1rem;
    padding-right: 1rem;
    scrollbar-width: none;

    &::-webkit-scrollbar {
      display: none;
    }
  }
}

.filter-btn {
  padding: 0.4rem 0.875rem;
  background: white;
  border: 1px solid $border-cream;
  border-radius: 999px;
  color: $brown-dark;
  font-family: inherit;
  font-size: 0.8125rem;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  flex-shrink: 0;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;

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
