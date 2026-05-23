<template>
  <div class="galaxy-search" role="search">
    <v-icon size="small" class="search-icon">mdi-magnify</v-icon>
    <input
      ref="inputEl"
      v-model="query"
      type="search"
      class="search-input"
      :placeholder="$t('galaxy.searchPlaceholder', 'Search the galaxy')"
      :aria-label="$t('galaxy.searchLabel', 'Search initiatives in the galaxy')"
      @input="onInput"
    >
    <button
      v-if="query"
      type="button"
      class="search-clear"
      :aria-label="$t('common.clear', 'Clear search')"
      @click="clear"
    >
      <v-icon size="small">mdi-close-circle</v-icon>
    </button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  nodes: GalaxyNode[]
}>()

const emit = defineEmits<{
  // Null when query is empty (no search active); otherwise an array of node ids
  // matching the query. Parent intersects this with the filter-visible set.
  match: [ids: number[] | null]
}>()

const { t: $t } = useI18n()
const inputEl = ref<HTMLInputElement | null>(null)
const query = ref('')
let debounceTimer: ReturnType<typeof setTimeout> | null = null

const normalize = (s: string) =>
  s
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()

const computeMatches = () => {
  const q = normalize(query.value.trim())
  if (!q) {
    emit('match', null)
    return
  }
  const ids: number[] = []
  for (const n of props.nodes) {
    if (normalize(n.slug).includes(q)) ids.push(n.id)
  }
  emit('match', ids)
}

const onInput = () => {
  if (debounceTimer) clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    debounceTimer = null
    computeMatches()
  }, 150)
}

const clear = () => {
  query.value = ''
  computeMatches()
  inputEl.value?.focus()
}

onBeforeUnmount(() => {
  if (debounceTimer) clearTimeout(debounceTimer)
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.galaxy-search {
  position: absolute;
  top: $spacing-sm;
  left: $spacing-sm;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  background: $galaxy-legend-bg;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: 999px;
  width: min(280px, calc(100% - #{$spacing-sm * 2}));
  z-index: 3;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);

  .search-icon {
    color: rgba(0, 0, 0, 0.55);
    flex-shrink: 0;
  }

  .search-input {
    flex: 1;
    min-width: 0;
    border: none;
    background: transparent;
    outline: none;
    font: inherit;
    font-size: 0.875rem;
    color: rgba(0, 0, 0, 0.87);

    &::placeholder {
      color: rgba(0, 0, 0, 0.45);
    }

    &:focus-visible {
      outline: none;
    }
  }

  &:focus-within {
    border-color: $green-bright;
    box-shadow: 0 0 0 2px rgba(76, 160, 73, 0.2);
  }

  .search-clear {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: transparent;
    border: none;
    cursor: pointer;
    padding: 0;
    color: rgba(0, 0, 0, 0.45);

    &:hover {
      color: $green-dark;
    }

    &:focus-visible {
      outline: 2px solid $green-dark;
      outline-offset: 2px;
      border-radius: 50%;
    }
  }
}
</style>
