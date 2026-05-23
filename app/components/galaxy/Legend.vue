<template>
  <details class="galaxy-legend" :open="defaultOpen">
    <summary>
      <v-icon size="x-small">mdi-palette-outline</v-icon>
      <span>{{ $t('galaxy.legendLabel', 'Continents') }}</span>
      <v-icon size="x-small" class="chevron">mdi-chevron-down</v-icon>
    </summary>
    <ul>
      <li v-for="entry in entries" :key="entry.key">
        <span class="swatch" :style="{ background: entry.color }" />
        <span class="continent-name">{{ entry.label }}</span>
      </li>
    </ul>
  </details>
</template>

<script setup lang="ts">
const props = defineProps<{
  continentColors: Record<string, string>
  presentContinents: string[] // only render legend rows for continents actually in view
  defaultOpen?: boolean
}>()

const { t: $t } = useI18n()

const continentLabel = (key: string): string => {
  const i18nKey = `projects.continents.${key}`
  const translated = $t(i18nKey)
  // Vue-i18n returns the key when translation is missing — fall back to a
  // tidier humanised version of the slug.
  if (translated === i18nKey) {
    return key
      .replace(/-/g, ' ')
      .replace(/\b\w/g, (c) => c.toUpperCase())
  }
  return translated
}

const entries = computed(() => {
  const present = new Set(props.presentContinents)
  return Object.entries(props.continentColors)
    .filter(([key]) => present.has(key))
    .map(([key, color]) => ({ key, color, label: continentLabel(key) }))
    .sort((a, b) => a.label.localeCompare(b.label))
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.galaxy-legend {
  position: absolute;
  left: $spacing-sm;
  bottom: $spacing-sm;
  background: $galaxy-legend-bg;
  border: 1px solid rgba(0, 0, 0, 0.08);
  border-radius: $galaxy-legend-radius;
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.78);
  z-index: 2;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  max-width: 220px;
}

summary {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 10px;
  cursor: pointer;
  list-style: none;
  font-weight: 600;
  color: $green-dark;

  &::-webkit-details-marker {
    display: none;
  }

  span {
    flex: 1;
  }

  .chevron {
    transition: transform 0.2s;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
    border-radius: $galaxy-legend-radius;
  }
}

.galaxy-legend[open] summary .chevron {
  transform: rotate(180deg);
}

ul {
  list-style: none;
  margin: 0;
  padding: 4px 10px 8px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  max-height: 180px;
  overflow-y: auto;
}

li {
  display: flex;
  align-items: center;
  gap: 8px;
}

.swatch {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.continent-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
