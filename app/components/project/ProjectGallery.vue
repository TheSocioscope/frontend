<template>
  <div v-if="resolvedGallery.length > 0" id="gallery" class="project-gallery">
    <span class="section-label">{{ $t('projects.detail.gallery') }}</span>

    <div class="gallery-grid">
      <button
        v-for="(item, index) in resolvedGallery"
        :key="index"
        class="gallery-item"
        type="button"
        @click="openLightbox(index)"
      >
        <img :src="item.url" :alt="item.caption || `Photo ${index + 1}`" class="gallery-img" loading="lazy" />
        <div class="gallery-overlay" aria-hidden="true">
          <v-icon size="24" color="white">mdi-magnify-plus-outline</v-icon>
        </div>
        <p v-if="item.caption" class="gallery-caption">{{ item.caption }}</p>
      </button>
    </div>

    <!-- Lightbox -->
    <div v-if="lightboxOpen" class="lightbox" role="dialog" aria-modal="true" @click.self="closeLightbox">
      <button class="lightbox-close" type="button" aria-label="Close" @click="closeLightbox">
        <v-icon color="white" size="24">mdi-close</v-icon>
      </button>
      <button
        v-if="currentIndex > 0"
        class="lightbox-nav lightbox-nav--prev"
        type="button"
        aria-label="Previous"
        @click="prevImage"
      >
        <v-icon color="white" size="28">mdi-chevron-left</v-icon>
      </button>
      <img
        :src="resolvedGallery[currentIndex].url"
        :alt="resolvedGallery[currentIndex].caption"
        class="lightbox-img"
      />
      <button
        v-if="currentIndex < resolvedGallery.length - 1"
        class="lightbox-nav lightbox-nav--next"
        type="button"
        aria-label="Next"
        @click="nextImage"
      >
        <v-icon color="white" size="28">mdi-chevron-right</v-icon>
      </button>
      <p v-if="resolvedGallery[currentIndex].caption" class="lightbox-caption">
        {{ resolvedGallery[currentIndex].caption }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  localizedGallery: Array<{ url: string; caption?: string }>
}>()

const { t: $t } = useI18n()
const runtimeConfig = useRuntimeConfig()
const baseURL = (runtimeConfig.app?.baseURL ?? '/').replace(/\/$/, '')

const resolveUrl = (url: string) =>
  url.startsWith('http://') || url.startsWith('https://') || url.startsWith('//')
    ? url
    : `${baseURL}${url.startsWith('/') ? url : `/${url}`}`

const resolvedGallery = computed(() =>
  (props.localizedGallery ?? []).map((item) => ({ ...item, url: resolveUrl(item.url) }))
)

const lightboxOpen = ref(false)
const currentIndex = ref(0)

const openLightbox = (index: number) => {
  currentIndex.value = index
  lightboxOpen.value = true
}

const closeLightbox = () => {
  lightboxOpen.value = false
}

const prevImage = () => {
  if (currentIndex.value > 0) currentIndex.value = currentIndex.value - 1
}

const nextImage = () => {
  if (currentIndex.value < resolvedGallery.value.length - 1)
    currentIndex.value = currentIndex.value + 1
}

// Keyboard navigation — registered directly in setup, cleaned up with onBeforeUnmount
const handleKey = (e: KeyboardEvent) => {
  if (!lightboxOpen.value) return
  if (e.key === 'Escape') closeLightbox()
  else if (e.key === 'ArrowLeft') prevImage()
  else if (e.key === 'ArrowRight') nextImage()
}

onMounted(() => window.addEventListener('keydown', handleKey))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKey))
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-gallery {
  margin-bottom: $rhythm-6;
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

.gallery-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.gallery-item {
  position: relative;
  aspect-ratio: 4/3;
  overflow: hidden;
  border-radius: 8px;
  border: none;
  padding: 0;
  cursor: pointer;
  background: $earth-10;

  &:hover .gallery-overlay {
    opacity: 1;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

.gallery-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;

  .gallery-item:hover & {
    transform: scale(1.04);
  }
}

.gallery-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.gallery-caption {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(0, 0, 0, 0.55);
  color: white;
  font-size: 11px;
  padding: 4px 8px;
  margin: 0;
  text-align: left;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* Lightbox */
.lightbox {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.9);
  z-index: $z-modal;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-close {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }
}

.lightbox-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(255, 255, 255, 0.15);
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease;

  &:hover {
    background: rgba(255, 255, 255, 0.3);
  }

  &--prev {
    left: 1rem;
  }

  &--next {
    right: 1rem;
  }
}

.lightbox-img {
  max-width: 90vw;
  max-height: 85vh;
  object-fit: contain;
  border-radius: 4px;
}

.lightbox-caption {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translateX(-50%);
  color: rgba(255, 255, 255, 0.85);
  font-size: 13px;
  background: rgba(0, 0, 0, 0.5);
  padding: 4px 12px;
  border-radius: 4px;
  margin: 0;
  white-space: nowrap;
}
</style>
