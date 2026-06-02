<template>
  <!-- Column mode: used inside the exchange board -->
  <div v-if="column" class="offers-column">
    <div class="col-header">
      <div class="col-header-icon col-header-icon--green" aria-hidden="true">
        <v-icon size="x-small" color="#2d5a0e">mdi-arrow-top-right</v-icon>
      </div>
      <span class="col-header-label col-header-label--green">
        {{ localizedName }} {{ $t('projects.detail.offers') }}
      </span>
    </div>
    <div class="offers-list">
      <component
        :is="offer.url ? 'a' : 'div'"
        v-for="(offer, index) in localizedOffers"
        :key="index"
        class="offer-card offer-card--green"
        :class="{ 'offer-card--link': offer.url }"
        :href="offer.url || undefined"
        :target="offer.url ? '_blank' : undefined"
        :rel="offer.url ? 'noopener noreferrer' : undefined"
      >
        <div class="offer-icon offer-icon--green" aria-hidden="true">
          <img v-if="offer.image" :src="offer.image" :alt="offer.title" class="offer-photo" />
          <v-icon v-else size="small" color="#2d5a0e">{{ getMdiIcon(offer.icon) }}</v-icon>
        </div>
        <div class="offer-body">
          <p class="offer-title offer-title--green">{{ offer.title }}</p>
          <p v-if="offer.description" class="offer-desc">{{ offer.description }}</p>
        </div>
        <v-icon v-if="offer.url" class="offer-link-icon" size="14">mdi-open-in-new</v-icon>
      </component>
    </div>
  </div>

  <!-- Standalone section mode (default) -->
  <section v-else id="offers" class="project-offers">
    <span class="section-label">{{ $t('projects.detail.offers') }}</span>
    <div class="offers-list">
      <component
        :is="offer.url ? 'a' : 'div'"
        v-for="(offer, index) in localizedOffers"
        :key="index"
        class="offer-card offer-card--green"
        :class="{ 'offer-card--link': offer.url }"
        :href="offer.url || undefined"
        :target="offer.url ? '_blank' : undefined"
        :rel="offer.url ? 'noopener noreferrer' : undefined"
      >
        <div class="offer-icon offer-icon--green" aria-hidden="true">
          <img v-if="offer.image" :src="offer.image" :alt="offer.title" class="offer-photo" />
          <v-icon v-else size="small" color="#2d5a0e">{{ getMdiIcon(offer.icon) }}</v-icon>
        </div>
        <div class="offer-body">
          <h3 class="offer-title offer-title--green">{{ offer.title }}</h3>
          <p v-if="offer.description" class="offer-desc">{{ offer.description }}</p>
        </div>
        <v-icon v-if="offer.url" class="offer-link-icon" size="14">mdi-open-in-new</v-icon>
      </component>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  localizedOffers: Array<{
    title: string
    description?: string
    image?: string
    url?: string
    icon?: string
  }>
  localizedName?: string
  column?: boolean
}>()

const { t: $t } = useI18n()

const getMdiIcon = (icon?: string): string => {
  if (!icon) return 'mdi-package-variant-closed'
  // Corrections for known invalid icon names used in the dataset
  const corrections: Record<string, string> = {
    'mdi-apple-food': 'mdi-food-apple',
  }
  if (corrections[icon]) return corrections[icon]
  // If already a full MDI icon name, pass through
  if (icon.startsWith('mdi-')) return icon
  const map: Record<string, string> = {
    fertilizer: 'mdi-sprout',
    feed: 'mdi-food-drumstick',
    training: 'mdi-school-outline',
    kit: 'mdi-gift-outline',
    consulting: 'mdi-lightbulb-outline',
    waste: 'mdi-recycle',
    group: 'mdi-account-group-outline',
    tech: 'mdi-robot-outline',
    plant: 'mdi-plant',
    bottle: 'mdi-bottle-tonic-outline',
    school: 'mdi-school-outline',
    map: 'mdi-map-outline',
  }
  return map[icon] || 'mdi-package-variant-closed'
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

/* ── Standalone section ─────────────────────────────────────── */
.project-offers {
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

/* ── Column mode header ─────────────────────────────────────── */
.offers-column {
  display: flex;
  flex-direction: column;
}

.col-header {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 9px;
}

.col-header-icon {
  width: 20px;
  height: 20px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &--green {
    background: rgba(76, 160, 73, 0.15);
  }
}

.col-header-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;

  &--green {
    color: $green-forest;
  }
}

/* ── Shared list + cards ────────────────────────────────────── */
.offers-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.offer-card {
  display: flex;
  align-items: center;
  gap: 12px;
  border-radius: 12px;
  padding: 12px 14px;
  text-decoration: none;

  &--green {
    background: rgba(76, 160, 73, 0.06);
    border: 0.5px solid rgba(76, 160, 73, 0.25);
  }

  /* Linkable card: pointer + hover lift */
  &--link {
    cursor: pointer;
    transition:
      background $transition-fast,
      border-color $transition-fast,
      box-shadow $transition-fast,
      transform $transition-fast;

    &:hover {
      background: rgba(76, 160, 73, 0.12);
      border-color: rgba(76, 160, 73, 0.5);
      box-shadow: 0 2px 8px rgba(76, 160, 73, 0.12);
      transform: translateY(-1px);

      .offer-link-icon {
        opacity: 1;
      }
    }

    &:focus-visible {
      outline: 2px solid $green-leaf;
      outline-offset: 2px;
    }
  }
}

.offer-icon {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  overflow: hidden;

  &--green {
    background: rgba(76, 160, 73, 0.18);
  }
}

/* Photo fills the circular badge */
.offer-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 50%;
  display: block;
}

.offer-body {
  flex: 1;
  min-width: 0;
}

.offer-title {
  font-size: 13px;
  font-weight: 600;
  margin: 0;
  line-height: 1.4;

  &--green {
    color: $earth-90;
  }
}

.offer-desc {
  font-size: 11px;
  color: $text-secondary;
  margin: 0;
  line-height: 1.4;
}

/* Link / connect indicator — always subtly visible, brighter on hover */
.offer-link-icon {
  color: $green-forest;
  opacity: 0.4;
  flex-shrink: 0;
  transition: opacity $transition-fast;
}

/* Reset <button> browser defaults so it looks identical to the <a> card */
button.offer-card {
  width: 100%;
  text-align: left;
  font-family: $font-family-base;
  font-size: inherit;
  cursor: pointer;
  appearance: none;
}

.offer-card--link:hover .offer-link-icon {
  opacity: 1;
}
</style>
