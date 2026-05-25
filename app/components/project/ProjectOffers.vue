<template>
  <section id="offers" class="project-offers">
    <ProjectSectionHeader icon="mdi-offer">
      {{ $t('projects.detail.offers') }}
    </ProjectSectionHeader>
    <ul class="offers-list">
      <li v-for="(offer, index) in localizedOffers" :key="index" class="offer-card">
        <div class="offer-icon" aria-hidden="true">{{ getEmoji(offer.icon) }}</div>
        <div class="offer-body">
          <h3 class="offer-title">{{ offer.title }}</h3>
          <p v-if="offer.description" class="offer-description">{{ offer.description }}</p>
        </div>
      </li>
    </ul>
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
}>()

const { t: $t } = useI18n()

const getEmoji = (icon?: string) => {
  if (!icon) return '📦'
  const emojiMap: Record<string, string> = {
    fertilizer: '🌱',
    feed: '🐔',
    training: '📚',
    kit: '🎁',
    consulting: '💡',
    waste: '♻️',
    group: '👥',
    tech: '🤖'
  }
  return emojiMap[icon] || '📦'
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-offers {
  margin-bottom: $rhythm-6;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $sticky-section-nav + $rhythm-2;

  @media (max-width: $detail-bp-tablet - 1) {
    margin-bottom: $rhythm-3;
  }
}

.offers-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: $rhythm-2;

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}

.offer-card {
  display: flex;
  align-items: flex-start;
  gap: $rhythm-2;
  padding: $rhythm-2;
  background: white;
  border: 1px solid $border-soft;
  border-radius: 8px;
  transition:
    border-color 0.15s,
    transform 0.15s,
    box-shadow 0.15s;

  &:hover {
    border-color: $green-leaf;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
  }

  @media (max-width: $detail-bp-tablet - 1) {
    padding: 10px 12px;
    gap: 10px;

    &:hover {
      transform: none;
      box-shadow: none;
    }
  }
}

.offer-icon {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 8px;
  background: $earth-10;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  line-height: 1;

  @media (max-width: $detail-bp-tablet - 1) {
    width: 36px;
    height: 36px;
    font-size: 1.25rem;
    border-radius: 6px;
  }
}

.offer-body {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.offer-title {
  margin: 0;
  font-family: $font-family-display;
  font-size: 1rem;
  font-weight: 600;
  color: $green-forest;
  line-height: 1.3;
  word-break: break-word;

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 0.9375rem;
  }
}

.offer-description {
  margin: 0;
  font-size: 0.875rem;
  line-height: 1.5;
  color: $text-secondary;
  /* 3-line clamp keeps cards uniform within the grid */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 0.8125rem;
    line-height: 1.45;
  }
}
</style>
