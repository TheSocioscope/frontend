<template>
  <section id="timeline" class="project-timeline">
    <div class="timeline-inner">
      <ProjectSectionHeader icon="mdi-timeline-text">
        {{ $t('projects.detail.timeline') }}
      </ProjectSectionHeader>
      <p class="timeline-hint">{{ $t('projects.detail.timelineHint') }}</p>

      <!-- Quick-jump year pills -->
      <div class="timeline-pills">
        <button
          v-for="(item, index) in localizedTimeline"
          :key="`pill-${index}`"
          type="button"
          class="timeline-pill"
          :class="{ 'is-active': index === activeIndex }"
          :style="
            index === activeIndex
              ? { background: accentFor(index), borderColor: accentFor(index) }
              : undefined
          "
          :aria-current="index === activeIndex ? 'true' : undefined"
          @click="scrollToCard(index)"
        >
          {{ item.date }}
        </button>
      </div>

      <!-- Snapping card strip -->
      <div ref="stripEl" class="timeline-strip" @scroll.passive="onScroll">
        <article
          v-for="(item, index) in localizedTimeline"
          :key="`card-${index}`"
          class="timeline-card"
          :class="{ 'is-active': index === activeIndex }"
          :style="{ '--card-accent': accentFor(index) }"
        >
          <div class="timeline-card-head">
            <span class="timeline-card-year">{{ item.date }}</span>
            <span v-if="item.icon" class="timeline-card-tag" aria-hidden="true">
              <v-icon size="x-small">{{ item.icon }}</v-icon>
            </span>
          </div>
          <p class="timeline-card-text">{{ item.text }}</p>
          <span class="timeline-card-counter" aria-hidden="true">{{ index + 1 }}/{{ total }}</span>
        </article>
      </div>

      <!-- Position progress bar -->
      <div class="timeline-bar" aria-hidden="true">
        <div
          class="timeline-bar-fill"
          :style="{
            width: `${((activeIndex + 1) / total) * 100}%`,
            background: accentFor(activeIndex)
          }"
        />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  localizedTimeline: Array<{ date: string; text: string; icon?: string }>
}>()

const { t: $t } = useI18n()

// Per-milestone accent — warm/earthy palette that sits well with the site's
// green + saffron + clay tokens; cycles if there are more than seven entries.
const ACCENTS = ['#4FA64B', '#D99A2B', '#C26B4F', '#5B8C7E', '#9C7BA8', '#6E8C45', '#C49A3A']
const accentFor = (i: number) => ACCENTS[((i % ACCENTS.length) + ACCENTS.length) % ACCENTS.length]

const total = computed(() => props.localizedTimeline.length)
const activeIndex = ref(0)
const stripEl = ref<HTMLElement | null>(null)

// Which card is closest to the centre of the scroll viewport?
let raf = 0
const onScroll = () => {
  if (raf) return
  raf = requestAnimationFrame(() => {
    raf = 0
    const strip = stripEl.value
    if (!strip) return
    const center = strip.scrollLeft + strip.clientWidth / 2
    let best = 0
    let bestDist = Infinity
    // .children skips the ::before/::after spacer pseudo-elements, so the
    // index here lines up 1:1 with localizedTimeline.
    for (let i = 0; i < strip.children.length; i++) {
      const card = strip.children[i] as HTMLElement
      const cardCenter = card.offsetLeft + card.offsetWidth / 2
      const d = Math.abs(cardCenter - center)
      if (d < bestDist) {
        bestDist = d
        best = i
      }
    }
    activeIndex.value = best
  })
}

const scrollToCard = (i: number) => {
  const strip = stripEl.value
  const card = strip?.children[i] as HTMLElement | undefined
  if (!strip || !card) return
  strip.scrollTo({
    left: card.offsetLeft + card.offsetWidth / 2 - strip.clientWidth / 2,
    behavior: 'smooth'
  })
}

onMounted(() => {
  onScroll()
  window.addEventListener('resize', onScroll, { passive: true })
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', onScroll)
  if (raf) cancelAnimationFrame(raf)
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

$tl-ease: cubic-bezier(0.4, 0, 0.2, 1);
$tl-pad: 28px;
$tl-pad-mobile: 16px;
$tl-card: min(82vw, 360px);

.project-timeline {
  margin-bottom: $rhythm-6;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $sticky-section-nav + $rhythm-2;
  background: #fafaf5;
  border-radius: 16px;
  padding: 32px 0;
  overflow: hidden; /* clip the bleeding strip to the rounded box */

  @media (max-width: $detail-bp-tablet - 1) {
    margin-bottom: $rhythm-3;
    padding: 20px 0;
    border-radius: 12px;
  }
}

/* Full-bleed cream band, but the actual content (header, pills, card strip,
   progress) stays in a centred, comfortably narrow column so the active card
   doesn't drift off into empty space on wide screens. */
.timeline-inner {
  box-sizing: border-box;
  max-width: 1040px;
  margin: 0 auto;
  padding: 0 $tl-pad;

  @media (max-width: $detail-bp-tablet - 1) {
    padding: 0 $tl-pad-mobile;
  }
}

.timeline-hint {
  margin: 6px 0 0;
  font-family: $font-family-base;
  font-size: 0.875rem;
  line-height: 1.5;
  color: $text-secondary;
}

/* ── Year pills ───────────────────────────────────────────────── */
.timeline-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 18px;
  padding-bottom: 2px; /* breathing room for focus rings */

  /* If they ever overflow (lots of milestones on a phone), scroll instead. */
  @media (max-width: $detail-bp-tablet - 1) {
    flex-wrap: nowrap;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;

    &::-webkit-scrollbar {
      display: none;
    }
  }
}

.timeline-pill {
  flex: 0 0 auto;
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid rgba(44, 36, 22, 0.18);
  background: #fff;
  color: $text-primary;
  font-family: $font-family-base;
  font-size: 0.8125rem;
  font-weight: 600;
  line-height: 1;
  white-space: nowrap;
  cursor: pointer;
  transition:
    background 0.35s $tl-ease,
    color 0.35s $tl-ease,
    border-color 0.35s $tl-ease,
    transform 0.2s $tl-ease;

  &:hover {
    border-color: rgba(44, 36, 22, 0.4);
  }

  &.is-active {
    color: #fff; /* background + border-color supplied inline (card accent) */
  }
}

/* ── Card strip ───────────────────────────────────────────────── */
.timeline-strip {
  position: relative;
  display: flex;
  align-items: stretch;
  gap: 16px;
  margin: 22px (-$tl-pad) 0;
  padding: 12px 0 26px;
  overflow-x: auto;
  overflow-y: hidden;
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;

  &::-webkit-scrollbar {
    display: none;
  }

  /* Spacers so the first and last cards can snap to the centre. */
  &::before,
  &::after {
    content: '';
    flex: 0 0 calc((100% - #{$tl-card}) / 2);
  }

  @media (max-width: $detail-bp-tablet - 1) {
    margin: 18px (-$tl-pad-mobile) 0;
  }
}

.timeline-card {
  flex: 0 0 $tl-card;
  box-sizing: border-box;
  scroll-snap-align: center;
  position: relative;
  background: #fff;
  border-radius: 16px;
  border-top: 4px solid var(--card-accent, #{$green-leaf});
  padding: 32px 28px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  opacity: 0.6;
  transform: scale(0.96);
  transform-origin: center bottom;
  transition:
    opacity 0.35s $tl-ease,
    transform 0.35s $tl-ease,
    box-shadow 0.35s $tl-ease;

  &.is-active {
    opacity: 1;
    transform: scale(1);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
  }

  @media (max-width: $detail-bp-tablet - 1) {
    padding: 26px 22px;
  }
}

.timeline-card-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 14px;
}

.timeline-card-year {
  font-family: $font-family-display;
  font-size: clamp(34px, 6vw, 48px);
  font-weight: $font-weight-bold;
  line-height: 1;
  color: $text-primary;
}

.timeline-card-tag {
  flex: 0 0 auto;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 999px;
  background: var(--card-accent, #{$green-leaf});
  color: #fff;
}

.timeline-card-text {
  margin: 0;
  font-family: $font-family-base;
  font-size: 15px;
  line-height: 1.65;
  color: $text-primary;
  word-break: break-word;
}

.timeline-card-counter {
  position: absolute;
  right: 16px;
  bottom: 12px;
  font-family: $font-family-base;
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  color: rgba(44, 36, 22, 0.35);
}

/* ── Progress bar ─────────────────────────────────────────────── */
.timeline-bar {
  margin-top: 4px;
  height: 3px;
  border-radius: 999px;
  background: #e8e4dc;
  overflow: hidden;
}

.timeline-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition:
    width 0.35s $tl-ease,
    background 0.35s $tl-ease;
}
</style>
