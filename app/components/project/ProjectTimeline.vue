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
          <span class="acc-year" :style="{ color: dateColor(index) }">{{ item.date }}</span>
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

// Cycle blue → pink → green for each date
const DATE_COLORS = ['#185FA5', '#C74B8E', '#2d7a2d']
const dateColor = (i: number) => DATE_COLORS[i % DATE_COLORS.length]

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
  /* Fixed date column — each button has its own grid, so "auto" would
     give each row a different column width. 130px safely fits the
     widest date ("1970s-1980s") and keeps all titles aligned. */
  display: grid;
  grid-template-columns: 130px 1fr auto;
  column-gap: $rhythm-3;
  align-items: center;
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
  /* color is set per-row via inline style */
  white-space: nowrap;
  line-height: 1;
}

.acc-title {
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
  transition: transform 0.2s ease;

  &.open {
    transform: rotate(180deg);
  }
}

.acc-body {
  display: none;
  padding: 0 4px $rhythm-3 calc(130px + #{$rhythm-3});

  &.open {
    display: block;
  }
}

.acc-text {
  font-size: 13px;
  color: $text-secondary;
  line-height: 1.7;
  margin: 0;
}
</style>
