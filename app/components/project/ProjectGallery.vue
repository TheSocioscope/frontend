<template>
  <v-card
    v-if="localizedGallery && localizedGallery.length > 0"
    id="gallery"
    class="project-gallery"
  >
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-image-multiple-outline</v-icon>
      {{ $t('common.gallery') }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col v-for="(item, index) in localizedGallery" :key="index" cols="12" sm="6" md="4">
          <v-card class="gallery-item" elevation="2" @click="openLightbox(index)">
            <v-img
              :src="item.url"
              :alt="item.caption || `Gallery image ${index + 1}`"
              aspect-ratio="1"
              cover
              class="gallery-image"
            >
              <div class="image-overlay">
                <v-icon size="large" color="white">mdi-magnify-plus-outline</v-icon>
              </div>
            </v-img>

            <v-card-text v-if="item.caption" class="gallery-caption">
              {{ item.caption }}
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <!-- Lightbox Dialog -->
      <v-dialog v-model="lightboxOpen" max-width="1200">
        <v-card>
          <v-card-text class="pa-0">
            <div class="lightbox-container">
              <v-btn icon class="lightbox-close" size="large" @click="lightboxOpen = false">
                <v-icon>mdi-close</v-icon>
              </v-btn>

              <v-btn
                v-if="currentIndex > 0"
                icon
                class="lightbox-nav lightbox-prev"
                size="large"
                @click="previousImage"
              >
                <v-icon>mdi-chevron-left</v-icon>
              </v-btn>

              <v-img
                :src="localizedGallery[currentIndex].url"
                :alt="localizedGallery[currentIndex].caption"
                max-height="80vh"
                contain
                class="lightbox-image"
              />

              <v-btn
                v-if="currentIndex < localizedGallery.length - 1"
                icon
                class="lightbox-nav lightbox-next"
                size="large"
                @click="nextImage"
              >
                <v-icon>mdi-chevron-right</v-icon>
              </v-btn>

              <div v-if="localizedGallery[currentIndex].caption" class="lightbox-caption">
                {{ localizedGallery[currentIndex].caption }}
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-dialog>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps<{
  localizedGallery: Array<{ url: string; caption?: string }>
}>()

const { t: $t } = useI18n()

const lightboxOpen = ref(false)
const currentIndex = ref(0)

const openLightbox = (index: number) => {
  currentIndex.value = index
  lightboxOpen.value = true
}

const previousImage = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

const nextImage = () => {
  if (currentIndex.value < props.localizedGallery.length - 1) {
    currentIndex.value++
  }
}

// Keyboard navigation
onMounted(() => {
  const handleKeyPress = (e: KeyboardEvent) => {
    if (!lightboxOpen.value) return

    if (e.key === 'Escape') {
      lightboxOpen.value = false
    } else if (e.key === 'ArrowLeft') {
      previousImage()
    } else if (e.key === 'ArrowRight') {
      nextImage()
    }
  }

  window.addEventListener('keydown', handleKeyPress)

  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyPress)
  })
})
</script>

<style scoped lang="scss">
.project-gallery {
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

.gallery-item {
  cursor: pointer;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;
  overflow: hidden;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2) !important;

    .image-overlay {
      opacity: 1;
    }
  }
}

.gallery-image {
  position: relative;
}

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.gallery-caption {
  font-size: 0.9rem;
  line-height: 1.4;
  color: rgba(0, 0, 0, 0.7);
  padding: 0.75rem;
}

.lightbox-container {
  position: relative;
  background: #000;
  min-height: 400px;
}

.lightbox-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 10;
  background: rgba(0, 0, 0, 0.5);
  color: white;

  &:hover {
    background: rgba(0, 0, 0, 0.7);
  }
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  z-index: 10;
  background: rgba(0, 0, 0, 0.5);
  color: white;

  &:hover {
    background: rgba(0, 0, 0, 0.7);
  }
}

.lightbox-prev {
  left: 1rem;
}

.lightbox-next {
  right: 1rem;
}

.lightbox-image {
  width: 100%;
}

.lightbox-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 1rem;
  text-align: center;
  font-size: 1rem;
}
</style>
