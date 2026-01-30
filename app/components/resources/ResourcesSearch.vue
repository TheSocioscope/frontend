<template>
  <div class="search-filter-section">
    <div class="search-bar">
      <span class="search-icon">🔍</span>
      <input
        v-model="localSearch"
        type="text"
        class="search-input"
        :placeholder="$t('resources.search.placeholder')"
        @input="handleSearch"
      />
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
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.search-filter-section {
  margin-bottom: 3rem;
}

.search-bar {
  position: relative;
  margin-bottom: 2rem;
}

.search-icon {
  position: absolute;
  left: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1.25rem;
  opacity: 0.6;
}

.search-input {
  width: 100%;
  padding: 1.25rem 1.5rem 1.25rem 4rem;
  border: 2px solid $border-cream;
  border-radius: 0;
  background: white;
  font-size: 1rem;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: $green-bright;
  }
}

.filter-buttons {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
}

.filter-btn {
  padding: 0.75rem 1.5rem;
  border: 2px solid $border-cream;
  background: white;
  border-radius: 0;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  color: $brown-dark;

  &:hover,
  &.active {
    background: $green-bright;
    color: white;
    border-color: $green-bright;
  }
}
</style>
