<template>
  <section class="section vision-section">
    <v-container>
      <div class="vision-header section-reveal">
        <h2 class="vision-title">{{ $t('vision.title') }}</h2>
        <div class="vision-statements">
          <p class="vision-statement">{{ $t('vision.statement1') }}</p>
          <p v-if="$t('vision.statement2')" class="vision-statement">
            {{ $t('vision.statement2') }}
          </p>
        </div>
      </div>

      <!-- Desktop: sleek 3-up grid · Phones: centred snapping card carousel -->
      <div class="contributions-grid section-reveal" ref="gridEl" @scroll.passive="onScroll">
        <button
          v-for="(icon, i) in contributionIcons"
          :key="i"
          type="button"
          class="contribution-card"
          :class="{ 'is-active': i === activeDot }"
          :aria-label="
            $t('common.readMoreAbout', 'Read more about') +
            ' ' +
            $t(`contributions.card${i + 1}.title`)
          "
          @click="openCard(i)"
        >
          <span class="contribution-icon" aria-hidden="true">
            <v-icon size="1.85rem">{{ icon }}</v-icon>
          </span>
          <h3 class="contribution-title">
            {{ $t(`contributions.card${i + 1}.title`) }}
          </h3>
          <p class="contribution-body contribution-body-clamp">
            {{ $t(`contributions.card${i + 1}.description`) }}
          </p>
          <span class="contribution-readmore">
            {{ $t('common.readMore', 'Read more') }}
            <v-icon size="x-small">mdi-arrow-right</v-icon>
          </span>
        </button>
      </div>

      <!-- Phones only: numbered pill nav for the carousel -->
      <div
        class="contribution-pills"
        :aria-label="$t('contributions.pagination', 'Carousel pagination')"
      >
        <button
          v-for="(icon, i) in contributionIcons"
          :key="i"
          type="button"
          class="contribution-pill"
          :class="{ 'is-active': i === activeDot }"
          :aria-current="i === activeDot ? 'true' : undefined"
          @click="goToCard(i)"
        >
          {{ $t(`contributions.card${i + 1}.title`) }}
        </button>
      </div>

      <!-- Phones only: position progress bar -->
      <div class="contribution-bar" aria-hidden="true">
        <div
          class="contribution-bar-fill"
          :style="{ width: `${((activeDot + 1) / contributionIcons.length) * 100}%` }"
        />
      </div>

      <!-- Tap-to-read modal: shows the full card content. Reuses Vuetify
           v-dialog. On mobile it slides up from the bottom; on desktop it centres. -->
      <v-dialog
        v-model="dialogOpen"
        max-width="640"
        transition="dialog-bottom-transition"
        scrim="rgba(44, 36, 22, 0.45)"
      >
        <div v-if="activeIndex !== null" class="contribution-dialog">
          <header class="dialog-header">
            <div class="dialog-icon">
              <v-icon size="1.75rem">{{ contributionIcons[activeIndex] }}</v-icon>
            </div>
            <h3 class="dialog-title">
              {{ $t(`contributions.card${activeIndex + 1}.title`) }}
            </h3>
            <button
              type="button"
              class="dialog-close"
              :aria-label="$t('common.close', 'Close')"
              @click="dialogOpen = false"
            >
              <v-icon>mdi-close</v-icon>
            </button>
          </header>
          <div class="dialog-body">
            <p>{{ $t(`contributions.card${activeIndex + 1}.description`) }}</p>
            <p v-if="$t(`contributions.card${activeIndex + 1}.description2`)">
              {{ $t(`contributions.card${activeIndex + 1}.description2`) }}
            </p>
            <a
              v-if="$t(`contributions.card${activeIndex + 1}.link`)"
              href="#"
              class="contribution-link"
            >
              {{ $t(`contributions.card${activeIndex + 1}.link`) }}
              <v-icon size="x-small">mdi-arrow-right</v-icon>
            </a>
          </div>
        </div>
      </v-dialog>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const contributionIcons = ['mdi-database-outline', 'mdi-chip', 'mdi-chart-line']

const dialogOpen = ref(false)
const activeIndex = ref<number | null>(null)

const openCard = (i: number) => {
  activeIndex.value = i
  dialogOpen.value = true
}

const gridEl = ref<HTMLElement | null>(null)
const activeDot = ref(0)

// Track the card nearest the scroll-viewport centre (the carousel snaps to
// centre on phones). Only meaningful while the strip actually scrolls; on the
// desktop grid it stays at 0 and the active styling is a no-op.
let frame = 0
const onScroll = () => {
  if (frame) return
  frame = requestAnimationFrame(() => {
    frame = 0
    const el = gridEl.value
    if (!el || el.scrollWidth <= el.clientWidth + 1) return
    const cards = el.querySelectorAll<HTMLElement>('.contribution-card')
    if (!cards.length) return
    const center = el.scrollLeft + el.clientWidth / 2
    let best = 0
    let bestDist = Infinity
    cards.forEach((card, i) => {
      const d = Math.abs(card.offsetLeft + card.offsetWidth / 2 - center)
      if (d < bestDist) {
        bestDist = d
        best = i
      }
    })
    activeDot.value = best
  })
}

const goToCard = (i: number) => {
  const el = gridEl.value
  const card = el?.querySelectorAll<HTMLElement>('.contribution-card')[i]
  if (!el || !card) return
  el.scrollTo({
    left: card.offsetLeft + card.offsetWidth / 2 - el.clientWidth / 2,
    behavior: 'smooth'
  })
}

onMounted(() => {
  onScroll()
  window.addEventListener('resize', onScroll, { passive: true })
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', onScroll)
  if (frame) cancelAnimationFrame(frame)
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

$vs-ease: cubic-bezier(0.4, 0, 0.2, 1);
$vs-card: min(82vw, 360px);

.vision-section {
  background: $surface-cream;
  padding: 3.5rem 0;

  @media (max-width: 768px) {
    padding: 2.25rem 0;
  }
}

/* Centered header — title and statements stacked, max-width capped. */
.vision-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 1rem;
  max-width: 760px;
  margin: 0 auto;
}

.vision-title {
  font-family: $font-family-display;
  font-size: 2rem;
  font-weight: $font-weight-bold;
  color: $brown-dark;
  line-height: 1.15;
  margin: 0;

  @media (max-width: 768px) {
    font-size: 1.5rem;
  }
}

.vision-statements {
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.vision-statement {
  font-size: 1rem;
  line-height: 1.65;
  color: $brown-dark;
  margin: 0;

  @media (max-width: 768px) {
    font-size: 0.9375rem;
  }
}

/* ── Card layout ──────────────────────────────────────────────── */
.contributions-grid {
  margin-top: 2.25rem;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  align-items: stretch;
  gap: $spacing-lg;

  @media (max-width: 960px) {
    grid-template-columns: repeat(2, 1fr);
  }

  /* Phones: horizontal scroll-snap carousel, centred. */
  @media (max-width: 600px) {
    margin-top: 1.75rem;
    display: flex;
    grid-template-columns: none;
    gap: 14px;
    margin-left: -16px; /* bleed past the v-container padding */
    margin-right: -16px;
    padding: 8px 0 4px;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    -webkit-overflow-scrolling: touch;
    scrollbar-width: none;

    &::-webkit-scrollbar {
      display: none;
    }

    /* Spacers so the first and last cards can snap to centre. */
    &::before,
    &::after {
      content: '';
      flex: 0 0 calc((100% - #{$vs-card}) / 2);
    }
  }
}

.contribution-card {
  /* Reset native button so it reads as a card */
  position: relative;
  box-sizing: border-box;
  background: #fff;
  border: none;
  border-top: 4px solid $green-bright;
  border-radius: 16px;
  padding: 28px 24px;
  font: inherit;
  text-align: left;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  height: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
  transition:
    transform 0.35s $vs-ease,
    box-shadow 0.35s $vs-ease,
    opacity 0.35s $vs-ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08);
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 3px;
  }

  /* Carousel-only emphasis: the centred card is full, neighbours recede. */
  @media (max-width: 600px) {
    flex: 0 0 $vs-card;
    scroll-snap-align: center;
    padding: 24px 20px;
    opacity: 0.6;
    transform: scale(0.96);
    transform-origin: center bottom;

    &:hover {
      transform: scale(0.96);
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
    }

    &.is-active {
      opacity: 1;
      transform: scale(1);
      box-shadow: 0 12px 40px rgba(0, 0, 0, 0.1);
    }
  }
}

.contribution-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(76, 160, 73, 0.12);
  color: $green-bright;
  margin-bottom: 1rem;

  @media (max-width: 600px) {
    width: 42px;
    height: 42px;
    margin-bottom: 0.75rem;
  }
}

.contribution-title {
  font-family: $font-family-display;
  font-size: 1.25rem;
  font-weight: 500;
  margin: 0 0 0.6rem;
  color: $green-forest;

  @media (max-width: 600px) {
    font-size: 1.0625rem;
  }
}

.contribution-body {
  font-family: $font-family-base;
  font-size: 0.9375rem;
  line-height: 1.6;
  color: $brown-medium;
  margin: 0 0 $spacing-sm;

  @media (max-width: 600px) {
    font-size: 0.875rem;
    line-height: 1.55;
  }
}

/* Body line-clamped on every viewport so cards stay uniform. Tap the card
   to open the modal with the full text. */
.contribution-body-clamp {
  display: -webkit-box;
  -webkit-line-clamp: 6;
  line-clamp: 6;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
  margin-bottom: $spacing-sm;

  @media (max-width: 600px) {
    -webkit-line-clamp: 5;
    line-clamp: 5;
  }
}

/* "Read more" affordance pinned to the card's bottom edge. */
.contribution-readmore {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  margin-top: auto;
  padding-top: $spacing-sm;
  font-family: $font-family-base;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: $green-bright;
  transition:
    color 0.2s,
    gap 0.2s;
}

.contribution-card:hover .contribution-readmore,
.contribution-card:focus-visible .contribution-readmore {
  color: $green-forest;
  gap: 8px;
}

/* ── Pill nav (phones only) ───────────────────────────────────── */
.contribution-pills {
  display: none;

  @media (max-width: 600px) {
    display: flex;
    align-items: center;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
  }
}

.contribution-pill {
  flex: 0 0 auto;
  padding: 7px 14px;
  border-radius: 999px;
  border: 1px solid rgba(76, 160, 73, 0.3);
  background: #fff;
  color: $green-forest;
  font-family: $font-family-base;
  font-size: 0.8125rem;
  font-weight: 600;
  line-height: 1;
  cursor: pointer;
  transition:
    background 0.35s $vs-ease,
    color 0.35s $vs-ease,
    border-color 0.35s $vs-ease;

  &.is-active {
    background: $green-bright;
    border-color: $green-bright;
    color: #fff;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
  }
}

/* ── Progress bar (phones only) ───────────────────────────────── */
.contribution-bar {
  display: none;

  @media (max-width: 600px) {
    display: block;
    margin: 12px 16px 0; /* match the card bleed inset */
    height: 3px;
    border-radius: 999px;
    background: rgba(76, 160, 73, 0.16);
    overflow: hidden;
  }
}

.contribution-bar-fill {
  height: 100%;
  border-radius: 999px;
  background: $green-bright;
  transition: width 0.35s $vs-ease;
}

/* ── Tap-to-read modal ────────────────────────────────────────── */
.contribution-dialog {
  background: #fff;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  max-height: 85vh;
  overflow: hidden;
}

.dialog-header {
  display: flex;
  align-items: center;
  gap: $spacing-sm;
  padding: $spacing-md $spacing-lg;
  border-bottom: 1px solid rgba(76, 160, 73, 0.14);
}

.dialog-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: rgba(76, 160, 73, 0.12);
  color: $green-bright;
  flex-shrink: 0;
}

.dialog-title {
  flex: 1;
  margin: 0;
  font-family: $font-family-display;
  font-size: 1.25rem;
  font-weight: 600;
  color: $green-forest;
  min-width: 0;
}

.dialog-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 50%;
  color: $green-bright;
  cursor: pointer;
  flex-shrink: 0;
  transition:
    background 0.15s,
    color 0.15s;

  &:hover {
    background: rgba(76, 160, 73, 0.1);
    color: $green-forest;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
  }
}

.dialog-body {
  padding: $spacing-md $spacing-lg $spacing-lg;
  overflow-y: auto;

  p {
    font-family: $font-family-base;
    font-size: 0.9375rem;
    line-height: 1.65;
    color: $brown-medium;
    margin: 0 0 $spacing-sm;

    &:last-of-type {
      margin-bottom: $spacing-md;
    }
  }
}

.contribution-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: $green-medium;
  text-decoration: none;
  font-family: $font-family-base;
  font-weight: $font-weight-medium;
  margin-top: $spacing-sm;
  transition: gap 0.3s;

  &:hover {
    gap: 10px;
  }
}
</style>
