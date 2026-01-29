<template>
  <v-card v-if="localizedOffers && localizedOffers.length > 0" id="offers" class="project-offers">
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-gift-outline</v-icon>
      {{ $t('common.offers') }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col v-for="(offer, index) in localizedOffers" :key="index" cols="12" md="6" lg="4">
          <v-card class="offer-card h-100" elevation="2">
            <v-img
              v-if="offer.image"
              :src="offer.image"
              :alt="offer.title"
              height="200"
              cover
              class="offer-image"
            >
              <div class="image-overlay" />
            </v-img>

            <v-card-title class="offer-title">
              {{ offer.title }}
            </v-card-title>

            <v-card-text>
              <div class="offer-description">{{ offer.description }}</div>

              <div v-if="offer.url" class="offer-link">
                <v-btn
                  :href="offer.url"
                  target="_blank"
                  variant="outlined"
                  size="small"
                  prepend-icon="mdi-open-in-new"
                >
                  {{ $t('common.learnMore') }}
                </v-btn>
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  localizedOffers: Array<{ title: string; description: string; image?: string; url?: string }>
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
.project-offers {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
}

.offer-card {
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
  }
}

.offer-image {
  position: relative;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.4) 100%);
}

.offer-title {
  font-size: 1.2rem;
  font-weight: 600;
  line-height: 1.3;
  padding: 1rem;
}

.offer-description {
  font-size: 1rem;
  line-height: 1.6;
  color: rgba(0, 0, 0, 0.7);
  margin-bottom: 1rem;
}

.offer-link {
  margin-top: 1rem;
}

.h-100 {
  height: 100%;
}
</style>
