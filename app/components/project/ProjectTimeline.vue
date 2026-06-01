<template>
  <section id="timeline" class="project-timeline">
    <span class="section-label">{{ $t('projects.detail.timeline') }}</span>
    <div class="accordion">
      <div v-for="(item, index) in localizedTimeline" :key="index" class="acc-item">
        <button
          type="button"
          class="acc-header"
          :aria-expanded="openItems.has(index)"
          @click="toggle(index)"
        >
          <span class="acc-year">{{ item.date }}</span>
          <div
            class="acc-icon-badge"
            :style="{ background: accentBg(index), color: accentColor(index) }"
            aria-hidden="true"
          >
            <v-icon size="x-small">{{ getIcon(item) }}</v-icon>
          </div>
          <span class="acc-title">{{ getTitle(item) }}</span>
          <v-icon class="acc-chevron" :class="{ open: openItems.has(index) }" size="small">
            mdi-chevron-down
          </v-icon>
        </button>
        <div class="acc-body" :class="{ open: openItems.has(index) }">
          <p class="acc-text">{{ item.text }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  localizedTimeline: Array<{ date: string; text: string; icon?: string; title?: string }>
}>()

const { t: $t } = useI18n()

// First item open by default
const openItems = ref<Set<number>>(new Set([0]))

const toggle = (i: number) => {
  const s = new Set(openItems.value)
  if (s.has(i)) s.delete(i)
  else s.add(i)
  openItems.value = s
}

const getTitle = (item: any): string => {
  if (item.title) return typeof item.title === 'string' ? item.title : (item.title.en ?? '')
  const text: string = item.text || ''
  if (text.length <= 60) return text
  const dotIdx = text.indexOf('. ')
  const dashIdx = text.indexOf(' — ')
  let cutoff = 60
  if (dotIdx > 10 && dotIdx < 80) cutoff = dotIdx
  else if (dashIdx > 10 && dashIdx < 80) cutoff = dashIdx
  return text.slice(0, cutoff) + '…'
}

// Alternating green / warm / blue accents
const BG = ['#e4f2d6', '#f3ede0', '#e4f2d6', '#e0ecf3', '#faeeda', '#e4f2d6', '#f3ede0']
const FG = ['#2d5a0e', '#854F0B', '#2d5a0e', '#185FA5', '#854F0B', '#2d5a0e', '#854F0B']
const accentBg = (i: number) => BG[i % BG.length]
const accentColor = (i: number) => FG[i % FG.length]

const ICON_MAP: Record<string, string> = {
  launch: 'mdi-rocket-launch-outline',
  founding: 'mdi-flag-checkered',
  founded: 'mdi-flag-checkered',
  start: 'mdi-play-circle-outline',
  award: 'mdi-trophy-outline',
  prize: 'mdi-trophy-outline',
  partnership: 'mdi-handshake-outline',
  funding: 'mdi-cash-multiple',
  grant: 'mdi-cash-multiple',
  expansion: 'mdi-map-marker-radius-outline',
  growth: 'mdi-trending-up',
  research: 'mdi-flask-outline',
  publication: 'mdi-book-open-outline',
  harvest: 'mdi-sprout',
  certification: 'mdi-certificate-outline',
  event: 'mdi-calendar-star',
  milestone: 'mdi-star-circle-outline',
  community: 'mdi-account-group-outline',
  training: 'mdi-school-outline',
  product: 'mdi-package-variant-closed',
  pilot: 'mdi-test-tube',
  legal: 'mdi-gavel',
}

const getIcon = (item: any): string => {
  const iconVal: string = item.icon || ''
  // If already a full MDI icon name, use it directly
  if (iconVal.startsWith('mdi-')) return iconVal
  // Look up short key in map
  if (ICON_MAP[iconVal]) return ICON_MAP[iconVal]
  // Try to infer from text content
  const text = (item.text || item.title || '').toLowerCase()
  if (text.includes('launch') || text.includes('lancé') || text.includes('lanzam')) return 'mdi-rocket-launch-outline'
  if (text.includes('found') || text.includes('créat') || text.includes('creat')) return 'mdi-flag-checkered'
  if (text.includes('award') || text.includes('prix') || text.includes('premio')) return 'mdi-trophy-outline'
  if (text.includes('partner') || text.includes('partenaire')) return 'mdi-handshake-outline'
  if (text.includes('fund') || text.includes('grant') || text.includes('financ')) return 'mdi-cash-multiple'
  if (text.includes('harvest') || text.includes('récolte')) return 'mdi-sprout'
  if (text.includes('certif')) return 'mdi-certificate-outline'
  if (text.includes('train') || text.includes('school') || text.includes('formation')) return 'mdi-school-outline'
  return 'mdi-circle-medium'
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-timeline {
  margin-bottom: $rhythm-6;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $rhythm-2;
}

.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $text-secondary;
  margin-bottom: $rhythm-2;
}

.accordion {
  border-top: 0.5px solid $border-soft;
}

.acc-item {
  border-bottom: 0.5px solid $border-soft;
}

.acc-header {
  display: flex;
  align-items: center;
  gap: $rhythm-2;
  width: 100%;
  padding: 14px 4px;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: $font-family-base;

  &:hover .acc-title {
    color: $green-forest;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

.acc-year {
  font-family: $font-family-display;
  font-size: 1.25rem;
  font-weight: $font-weight-semibold; /* 600 — only loaded weight for Playfair */
  color: $green-forest;
  min-width: 56px;
  flex-shrink: 0;
  line-height: 1;
}

.acc-icon-badge {
  width: 28px;
  height: 28px;
  border-radius: 7px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

.acc-title {
  flex: 1;
  font-size: 14px;
  font-weight: 700;
  color: $text-primary;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: color $transition-fast;
}

.acc-chevron {
  color: $text-caption;
  flex-shrink: 0;
  transition: transform 0.2s ease;

  &.open {
    transform: rotate(180deg);
  }
}

/* Indent body to align with title column */
.acc-body {
  display: none;
  padding: 0 4px $rhythm-3 calc(56px + #{$rhythm-2} + 28px + #{$rhythm-2});

  &.open {
    display: block;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    padding-left: $rhythm-3;
  }
}

.acc-text {
  font-size: 13px;
  color: $text-secondary;
  line-height: 1.7;
  margin: 0;
}
</style>
