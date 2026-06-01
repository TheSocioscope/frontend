<template>
  <section v-if="related.length > 0" class="project-related">
    <div class="related-header">
      <span class="section-label">{{ $t('projects.related', 'Similar initiatives') }}</span>
      <p class="related-subtitle">
        {{ $t('projects.relatedHint', 'By country, sector, and region') }}
      </p>
    </div>
    <div class="related-grid">
      <NuxtLink
        v-for="p in related"
        :key="p.pubId"
        :to="localePath(`/projects/${getSlug(p)}`)"
        class="sim-card"
      >
        <div class="sim-card-left">
          <div class="sim-dot" :style="{ background: avatarBg(p.pubId) }">
            {{ getInitials(getName(p)) }}
          </div>
          <div class="sim-info">
            <p class="sim-name">{{ getName(p) }}</p>
            <p v-if="p.location || p.country?.length" class="sim-meta">
              {{ p.location || getCountryLabel((p.country || [])[0]) }}
            </p>
          </div>
        </div>
        <v-icon class="sim-arrow" size="small">mdi-arrow-right</v-icon>
      </NuxtLink>
    </div>
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

const { data: candidates } = await useAsyncData(
  `related-${props.currentProject?.pubId ?? 0}`,
  () =>
    queryCollection('projects')
      .select('pubId', 'name', 'country', 'continent', 'sectorFocus', 'location')
      .all() as Promise<any[]>
)

const related = computed(() => {
  if (!candidates.value || !props.currentProject) return []
  const cur = props.currentProject
  const curCountries = new Set(cur.country || [])
  const curContinents = new Set(cur.continent || [])
  const curSectors = new Set(cur.sectorFocus || [])

  return candidates.value
    .filter((p) => p.pubId !== cur.pubId)
    .map((p) => {
      let score = 0
      score += (p.country || []).filter((c: string) => curCountries.has(c)).length * 3
      score += (p.sectorFocus || []).filter((s: string) => curSectors.has(s)).length * 2
      score += (p.continent || []).filter((c: string) => curContinents.has(c)).length * 1
      return { project: p, score }
    })
    .filter((e) => e.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 4)
    .map((e) => e.project)
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-related {
  margin-top: $rhythm-6;
  padding-top: $rhythm-4;
  border-top: 0.5px solid $border-soft;
}

.related-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: $rhythm-3;
  flex-wrap: wrap;
  gap: $rhythm-1;
}

.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $text-secondary;
  margin-bottom: 2px;
}

.related-subtitle {
  font-size: 13px;
  color: $text-caption;
  margin: 0;
}

.related-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;

  @media (max-width: $detail-bp-desktop - 1) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: 1fr;
  }
}

.sim-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: $rhythm-2;
  padding: 14px 16px;
  background: white;
  border: 0.5px solid $border-soft;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
  transition: border-color $transition-fast;

  &:hover {
    border-color: $green-forest;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

.sim-card-left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.sim-dot {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  color: white;
  flex-shrink: 0;
}

.sim-info {
  min-width: 0;
}

.sim-name {
  font-size: 13px;
  font-weight: 700;
  color: $text-primary;
  margin: 0 0 2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sim-meta {
  font-size: 11px;
  color: $text-secondary;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sim-arrow {
  color: $text-caption;
  flex-shrink: 0;
}
</style>
