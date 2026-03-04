<template>
  <v-card class="project-offers mb-4" elevation="2" id="offers">
    <ProjectSectionHeader icon="mdi-offer">
      {{ $t('projects.detail.offers') }}
    </ProjectSectionHeader>

    <v-card-text>
      <div class="products-grid">
        <div v-for="(offer, index) in localizedOffers" :key="index" class="product-card">
          <div class="product-image">
            <div class="product-placeholder">{{ getEmoji(offer.icon) }}</div>
          </div>
          <div class="product-content">
            <h3>{{ offer.title }}</h3>
            <p v-if="offer.description">{{ offer.description }}</p>
          </div>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps<{
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
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
}

.product-card {
  background-color: #f5edd6;
  border-radius: 12px;
  overflow: hidden;
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  border: 2px solid #4ca049;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 20px rgba(76, 160, 73, 0.2);
  }
}

.product-image {
  background-color: #fffbf0;
  padding: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 150px;
}

.product-placeholder {
  font-size: 4em;
  color: #4ca049;
}

.product-content {
  padding: 20px;

  h3 {
    color: #27421d;
    font-size: 1.3em;
    margin-bottom: 10px;
    font-weight: 700;
  }

  p {
    color: #2c2416;
    line-height: 1.6;
    margin: 0;
  }
}
</style>
