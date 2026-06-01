<template>
  <!-- Column mode: used inside the exchange board -->
  <div v-if="column" class="offers-column">
    <div class="col-header">
      <div class="col-header-icon col-header-icon--green" aria-hidden="true">
        <v-icon size="x-small" color="#2d5a0e">mdi-arrow-top-right</v-icon>
      </div>
      <span class="col-header-label col-header-label--green">
        {{ $t('projects.detail.offers') }}
      </span>
    </div>
    <div class="offers-list">
      <div v-for="(offer, index) in localizedOffers" :key="index" class="offer-card offer-card--green">
        <div class="offer-icon offer-icon--green" aria-hidden="true">
          <v-icon size="small" color="#2d5a0e">{{ getMdiIcon(offer.icon) }}</v-icon>
        </div>
        <div class="offer-body">
          <p class="offer-title offer-title--green">{{ offer.title }}</p>
          <p v-if="offer.description" class="offer-desc">{{ offer.description }}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Standalone section mode (default) -->
  <section v-else id="offers" class="project-offers">
    <span class="section-label">{{ $t('projects.detail.offers') }}</span>
    <div class="offers-list">
      <div v-for="(offer, index) in localizedOffers" :key="index" class="offer-card offer-card--green">
        <div class="offer-icon offer-icon--green" aria-hidden="true">
          <v-icon size="small" color="#2d5a0e">{{ getMdiIcon(offer.icon) }}</v-icon>
        </div>
        <div class="offer-body">
          <h3 class="offer-title offer-title--green">{{ offer.title }}</h3>
          <p v-if="offer.description" class="offer-desc">{{ offer.description }}</p>
        </div>
      </div>
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
  column?: boolean
}>()

const { t: $t } = useI18n()

const getMdiIcon = (icon?: string): string => {
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
  return map[icon || ''] || 'mdi-package-variant-closed'
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
  align-items: flex-start;
  gap: 10px;
  border-radius: 12px;
  padding: 12px 14px;

  &--green {
    background: rgba(76, 160, 73, 0.06);
    border: 0.5px solid rgba(76, 160, 73, 0.25);
  }
}

.offer-icon {
  width: 30px;
  height: 30px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &--green {
    background: rgba(76, 160, 73, 0.12);
  }
}

.offer-body {
  flex: 1;
  min-width: 0;
}

.offer-title {
  font-size: 13px;
  font-weight: 700;
  margin: 0 0 1px;
  line-height: 1.3;

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
</style>
