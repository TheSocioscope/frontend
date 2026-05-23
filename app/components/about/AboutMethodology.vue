<template>
  <section class="section methodology-section">
    <v-container>
      <header class="method-head section-reveal">
        <h2>{{ $t('about.methodology.title') }}</h2>
        <p>{{ $t('about.methodology.subtitle') }}</p>
      </header>

      <!-- Desktop: sleek 4-up grid · Phones: snapping card carousel -->
      <div ref="track" class="method-grid section-reveal" @scroll.passive="onScroll">
        <article
          v-for="(method, index) in methods"
          :key="index"
          class="method-card"
          :class="{ 'is-active': index === activeIndex }"
          :style="{ '--card-accent': accentFor(index) }"
        >
          <span class="method-number">{{ pad(index + 1) }}</span>
          <h3>{{ $t(method.titleKey) }}</h3>
          <p>{{ $t(method.descKey) }}</p>
        </article>
      </div>

      <!-- Phones only: numbered pill nav for the carousel -->
      <div class="method-pills">
        <button
          v-for="(method, index) in methods"
          :key="index"
          type="button"
          class="method-pill"
          :class="{ 'is-active': index === activeIndex }"
          :style="
            index === activeIndex
              ? { background: accentFor(index), borderColor: accentFor(index) }
              : undefined
          "
          :aria-label="$t(method.titleKey)"
          :aria-current="index === activeIndex ? 'true' : undefined"
          @click="scrollTo(index)"
        >
          {{ pad(index + 1) }}
        </button>
      </div>

      <!-- Phones only: position progress bar -->
      <div class="method-bar" aria-hidden="true">
        <div
          class="method-bar-fill"
          :style="{
            width: `${((activeIndex + 1) / methods.length) * 100}%`,
            background: accentFor(activeIndex)
          }"
        />
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const methods = [
  { titleKey: 'about.methodology.step1.title', descKey: 'about.methodology.step1.desc' },
  { titleKey: 'about.methodology.step2.title', descKey: 'about.methodology.step2.desc' },
  { titleKey: 'about.methodology.step3.title', descKey: 'about.methodology.step3.desc' },
  { titleKey: 'about.methodology.step4.title', descKey: 'about.methodology.step4.desc' }
]

// Same warm/earthy accent palette as the project timeline carousel.
const ACCENTS = ['#4FA64B', '#D99A2B', '#C26B4F', '#5B8C7E', '#9C7BA8', '#6E8C45', '#C49A3A']
const accentFor = (i: number) => ACCENTS[((i % ACCENTS.length) + ACCENTS.length) % ACCENTS.length]

const pad = (n: number) => String(n).padStart(2, '0')

const track = ref<HTMLElement | null>(null)
const activeIndex = ref(0)

// Track the centred card — only meaningful when the strip actually scrolls
// (phones); on the desktop grid it stays at 0 and the active styling is a no-op.
let frame = 0
const onScroll = () => {
  if (frame) return
  frame = requestAnimationFrame(() => {
    frame = 0
    const el = track.value
    if (!el || el.scrollWidth <= el.clientWidth + 1) return
    const center = el.scrollLeft + el.clientWidth / 2
    let best = 0
    let bestDist = Infinity
    for (let i = 0; i < el.children.length; i++) {
      const card = el.children[i] as HTMLElement
      const d = Math.abs(card.offsetLeft + card.offsetWidth / 2 - center)
      if (d < bestDist) {
        bestDist = d
        best = i
      }
    }
    activeIndex.value = best
  })
}

const scrollTo = (index: number) => {
  const el = track.value
  const card = el?.children[index] as HTMLElement | undefined
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
@use '../../../assets/styles/variables' as *;

$mt-ease: cubic-bezier(0.4, 0, 0.2, 1);
$mt-card: min(82vw, 360px);

.methodology-section {
  background: $cream;
  padding: 3rem 0;
  border-top: 1px solid $warm-beige;
  border-bottom: 1px solid $warm-beige;

  @media (max-width: 768px) {
    padding: 2.25rem 0;
  }
}

/* ── Header ───────────────────────────────────────────────────── */
.method-head {
  text-align: center;
  max-width: 640px;
  margin: 0 auto 2rem;

  h2 {
    margin: 0 0 0.5rem;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    font-size: clamp(1.75rem, 4vw, 2.6rem);
    line-height: 1.2;
    color: $brown-dark;
  }

  p {
    margin: 0;
    font-family: $font-family-display;
    font-size: clamp(0.95rem, 1.4vw, 1.1rem);
    line-height: 1.55;
    color: $brown-dark;
    opacity: 0.7;
  }

  @media (max-width: 768px) {
    margin-bottom: 1.5rem;
  }
}

/* ── Card layout ──────────────────────────────────────────────── */
.method-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  align-items: stretch;
  gap: 1.25rem;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(2, 1fr);
  }

  /* Phones: horizontal scroll-snap carousel, centred. */
  @media (max-width: 600px) {
    display: flex;
    grid-template-columns: none;
    gap: 14px;
    margin: 0 -16px; /* bleed past the v-container padding */
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
      flex: 0 0 calc((100% - #{$mt-card}) / 2);
    }
  }
}

.method-card {
  position: relative;
  box-sizing: border-box;
  background: #fff;
  border: 1px solid $cream-dark;
  border-top: 4px solid var(--card-accent, #{$green-bright});
  border-radius: 16px;
  padding: 28px 24px;
  box-shadow: 0 2px 8px rgba(44, 36, 22, 0.04);
  transition:
    transform 0.35s $mt-ease,
    box-shadow 0.35s $mt-ease,
    opacity 0.35s $mt-ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 32px rgba(44, 36, 22, 0.08);
  }

  .method-number {
    display: block;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    font-size: clamp(2rem, 3.4vw, 2.75rem);
    line-height: 1;
    color: var(--card-accent, #{$green-bright});
    margin-bottom: 0.625rem;
    letter-spacing: 0.01em;
  }

  h3 {
    margin: 0 0 0.4rem;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    font-size: 1.0625rem;
    line-height: 1.3;
    color: $brown-dark;
  }

  p {
    margin: 0;
    font-family: $font-family-display;
    font-size: 0.875rem;
    line-height: 1.6;
    color: $brown-dark;
    opacity: 0.78;
    word-break: break-word;
  }

  /* Carousel-only emphasis: the centred card is full, neighbours recede. */
  @media (max-width: 600px) {
    flex: 0 0 $mt-card;
    scroll-snap-align: center;
    padding: 26px 22px;
    opacity: 0.6;
    transform: scale(0.96);
    transform-origin: center bottom;

    &:hover {
      transform: scale(0.96);
      box-shadow: 0 2px 8px rgba(44, 36, 22, 0.04);
    }

    &.is-active {
      opacity: 1;
      transform: scale(1);
      box-shadow: 0 12px 40px rgba(44, 36, 22, 0.1);
    }
  }
}

/* ── Pill nav (phones only) ───────────────────────────────────── */
.method-pills {
  display: none;

  @media (max-width: 600px) {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    margin-top: 16px;
  }
}

.method-pill {
  flex: 0 0 auto;
  padding: 7px 13px;
  border-radius: 999px;
  border: 1px solid rgba(44, 36, 22, 0.18);
  background: #fff;
  color: $brown-dark;
  font-family: $font-family-display;
  font-size: 0.78rem;
  font-weight: $font-weight-bold;
  letter-spacing: 0.04em;
  line-height: 1;
  cursor: pointer;
  transition:
    background 0.35s $mt-ease,
    color 0.35s $mt-ease,
    border-color 0.35s $mt-ease;

  &.is-active {
    color: #fff; /* background + border supplied inline (card accent) */
  }
}

/* ── Progress bar (phones only) ───────────────────────────────── */
.method-bar {
  display: none;

  @media (max-width: 600px) {
    display: block;
    margin: 12px 16px 0; /* match the card bleed inset */
    height: 3px;
    border-radius: 999px;
    background: #e8e4dc;
    overflow: hidden;
  }
}

.method-bar-fill {
  height: 100%;
  border-radius: 999px;
  transition:
    width 0.35s $mt-ease,
    background 0.35s $mt-ease;
}
</style>
