<template>
  <section v-if="related.length > 0" class="project-related">
    <div class="related-header">
      <span class="section-label">{{ $t('projects.related', 'Similar initiatives') }}</span>
      <p class="related-subtitle">
        {{ $t('projects.relatedHint', 'By country, sector, and region') }}
      </p>
    </div>

    <div class="carousel-wrapper">
      <!-- Carousel container -->
      <div class="carousel-container" ref="carouselRef">
        <div class="carousel-track" :style="{ transform: `translateX(${carouselOffset}px)` }">
          <NuxtLink
            v-for="p in related"
            :key="p.pubId"
            :to="localePath(`/projects/${getSlug(p)}`)"
            class="sim-card"
          >
            <div class="sim-thumb">
              <img
                v-if="p.yt"
                :src="`https://img.youtube.com/vi/${p.yt}/mqdefault.jpg`"
                class="sim-thumb-img"
                alt=""
                loading="lazy"
              />
              <div
                v-else
                class="sim-thumb-placeholder"
                :style="{ background: avatarBg(p.pubId) }"
              >
                {{ getInitials(getName(p)) }}
              </div>
            </div>
            <div class="sim-body">
              <p class="sim-name">{{ getName(p) }}</p>
              <p v-if="p.location || p.country?.length" class="sim-meta">
                {{ p.location || getCountryLabel((p.country || [])[0]) }}
              </p>
            </div>
          </NuxtLink>
        </div>
      </div>

      <!-- Navigation arrows -->
      <button
        v-if="canScrollLeft"
        class="carousel-arrow carousel-arrow--prev"
        @click="scrollLeft"
        :aria-label="$t('common.previous', 'Previous')"
      >
        <v-icon>mdi-chevron-left</v-icon>
      </button>
      <button
        v-if="canScrollRight"
        class="carousel-arrow carousel-arrow--next"
        @click="scrollRight"
        :aria-label="$t('common.next', 'Next')"
      >
        <v-icon>mdi-chevron-right</v-icon>
      </button>
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

const carouselRef = ref<HTMLElement | null>(null)
const carouselOffset = ref(0)
const canScrollLeft = ref(false)
const canScrollRight = ref(true)

const CARD_WIDTH = 220 // Width of each card + gap
const VISIBLE_CARDS = 4 // Number of cards visible at once

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
      .select('pubId', 'name', 'country', 'continent', 'sectorFocus', 'location', 'yt')
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
      // Prioritize matches in BOTH country and sector
      const countryMatches = (p.country || []).filter((c: string) => curCountries.has(c)).length
      const sectorMatches = (p.sectorFocus || []).filter((s: string) => curSectors.has(s)).length
      const continentMatches = (p.continent || []).filter((c: string) => curContinents.has(c)).length

      // Give higher score for items matching sectors (important!)
      score += sectorMatches * 5

      // Add country matches but slightly lower weight
      score += countryMatches * 4

      // Continental matches as tiebreaker
      score += continentMatches * 1

      return { project: p, score }
    })
    .filter((e) => e.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, 12) // Show up to 12 items
    .map((e) => e.project)
})

// Update scroll button visibility
const updateScrollButtons = () => {
  canScrollLeft.value = carouselOffset.value < 0
  canScrollRight.value =
    Math.abs(carouselOffset.value) < (related.value.length - VISIBLE_CARDS) * CARD_WIDTH
}

const scrollLeft = () => {
  carouselOffset.value = Math.min(carouselOffset.value + CARD_WIDTH * 2, 0)
  updateScrollButtons()
}

const scrollRight = () => {
  const maxScroll = -(related.value.length - VISIBLE_CARDS) * CARD_WIDTH
  carouselOffset.value = Math.max(carouselOffset.value - CARD_WIDTH * 2, maxScroll)
  updateScrollButtons()
}

// Watch related items to update buttons
watch(related, () => {
  carouselOffset.value = 0
  updateScrollButtons()
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

/* Carousel wrapper */
.carousel-wrapper {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
}

.carousel-container {
  overflow: hidden;
  flex: 1;
}

.carousel-track {
  display: flex;
  gap: 10px;
  transition: transform 0.3s ease-out;
}

/* Vertical card with thumbnail on top */
.sim-card {
  display: flex;
  flex-direction: column;
  background: white;
  border: 0.5px solid $border-soft;
  border-radius: 12px;
  text-decoration: none;
  color: inherit;
  overflow: hidden;
  transition:
    border-color $transition-fast,
    box-shadow $transition-fast;
  flex-shrink: 0;
  width: 200px;

  &:hover {
    border-color: $green-forest;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.07);
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

.sim-thumb {
  width: 100%;
  aspect-ratio: 16 / 9;
  overflow: hidden;
  background: $earth-10;
  flex-shrink: 0;
}

.sim-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;

  .sim-card:hover & {
    transform: scale(1.04);
  }
}

.sim-thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: $font-family-display;
  font-size: 1.25rem;
  font-weight: 700;
  color: white;
}

.sim-body {
  padding: 10px 12px 12px;
  flex: 1;
}

.sim-name {
  font-size: 13px;
  font-weight: 700;
  color: $text-primary;
  margin: 0 0 3px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.35;
}

.sim-meta {
  font-size: 11px;
  color: $text-secondary;
  margin: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Carousel navigation arrows */
.carousel-arrow {
  position: relative;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: white;
  border: 0.5px solid $border-soft;
  border-radius: 50%;
  cursor: pointer;
  transition:
    background $transition-fast,
    border-color $transition-fast;
  color: $green-forest;

  &:hover {
    background: $earth-5;
    border-color: $green-forest;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }

  &:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    width: 36px;
    height: 36px;
  }
}

.carousel-arrow--prev {
  // Left arrow
}

.carousel-arrow--next {
  // Right arrow
}
</style>
