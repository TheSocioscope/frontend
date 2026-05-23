<template>
  <section v-if="related.length > 0" class="project-related">
    <h3 class="related-title">{{ $t('projects.related', 'Similar initiatives') }}</h3>
    <p class="related-subtitle">
      {{ $t('projects.relatedHint', 'By country, sector, and region') }}
    </p>
    <ul class="related-list">
      <li v-for="p in related" :key="p.pubId">
        <NuxtLink :to="localePath(`/projects/${getSlug(p)}`)" class="related-row">
          <span class="related-avatar" :style="{ background: avatarBg(p.pubId) }">
            {{ getInitials(getName(p)) }}
          </span>
          <span class="related-body">
            <span class="related-name">{{ getName(p) }}</span>
            <span v-if="p.location || p.country?.length" class="related-meta">
              <v-icon size="x-small">mdi-map-marker</v-icon>
              {{ p.location || getCountryLabel((p.country || [])[0]) }}
            </span>
          </span>
          <v-icon class="related-arrow" size="small">mdi-chevron-right</v-icon>
        </NuxtLink>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  currentProject: any
}>()

const { t: $t } = useI18n()
const localePath = useLocalePath()
const { getCountryLabel } = useProjectMappings()

const slugify = (text: string) =>
  text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 80)

const getName = (p: any): string => {
  if (!p?.name) return ''
  if (typeof p.name === 'string') return p.name
  return p.name.en || Object.values(p.name)[0] || ''
}

const getSlug = (p: any): string => slugify(getName(p))

const getInitials = (name: string): string => {
  const words = name.trim().split(/\s+/)
  return words.length >= 2
    ? (words[0][0] + words[1][0]).toUpperCase()
    : name.slice(0, 2).toUpperCase()
}

const avatarBg = (pubId: number): string => {
  const colors = ['#27421d', '#4ca049', '#5c4a2f', '#6b8e23', '#8b6f47']
  return colors[pubId % colors.length]
}

// Lightweight fetch — just the fields we need to score and render rows.
const { data: candidates } = await useAsyncData(
  `related-${props.currentProject?.pubId ?? 0}`,
  () =>
    queryCollection('projects')
      .select('pubId', 'name', 'country', 'continent', 'sectorFocus', 'location')
      .all() as Promise<any[]>
)

// Score candidates by relevance to the current project. Country is the
// strongest signal; shared sectors next; same continent is a tiebreaker.
const related = computed(() => {
  if (!candidates.value || !props.currentProject) return []
  const cur = props.currentProject
  const curCountries = new Set(cur.country || [])
  const curContinents = new Set(cur.continent || [])
  const curSectors = new Set(cur.sectorFocus || [])

  const scored = candidates.value
    .filter((p) => p.pubId !== cur.pubId)
    .map((p) => {
      let score = 0
      const sharedCountries = (p.country || []).filter((c: string) => curCountries.has(c)).length
      const sharedSectors = (p.sectorFocus || []).filter((s: string) => curSectors.has(s)).length
      const sharedContinents = (p.continent || []).filter((c: string) => curContinents.has(c))
        .length
      score += sharedCountries * 3
      score += sharedSectors * 2
      score += sharedContinents * 1
      return { project: p, score }
    })
    .filter((entry) => entry.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 5)
    .map((entry) => entry.project)

  return scored
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-related {
  margin-top: $rhythm-3;
  padding: $rhythm-2 $rhythm-3 $rhythm-3;
  background: white;
  border: 1px solid $border-soft;
  border-radius: 12px;

  @media (max-width: $detail-bp-tablet - 1) {
    border-radius: 8px;
    padding: $rhythm-2;
  }
}

.related-title {
  margin: 0 0 2px;
  font-family: $font-family-display;
  font-size: 1rem;
  font-weight: 700;
  color: $green-forest;
}

.related-subtitle {
  margin: 0 0 $rhythm-2;
  font-size: 0.75rem;
  color: $text-caption;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.related-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.related-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 8px 6px;
  border-radius: 6px;
  text-decoration: none;
  color: inherit;
  transition: background 0.15s;

  &:hover {
    background: $earth-10;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }

  & + .related-row {
    border-top: 1px solid $border-soft;
  }
}

.related-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.03em;
}

.related-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.related-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: $text-primary;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.related-meta {
  font-size: 0.75rem;
  color: $text-caption;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.related-arrow {
  color: $text-disabled;
  flex-shrink: 0;
}

li:not(:first-child) .related-row {
  border-top: 1px solid $border-soft;
}
</style>
