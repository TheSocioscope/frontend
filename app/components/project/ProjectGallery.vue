<template>
  <section id="gallery" class="project-gallery">
    <span class="section-label">{{ $t('projects.detail.video') }}</span>

    <!-- Placeholder when no media -->
    <div v-if="!items.length" class="gallery-placeholder">
      <v-icon size="64" color="#4ca049">mdi-image-plus</v-icon>
      <h3>Add photos &amp; videos</h3>
      <p>Share visual content to showcase your initiative</p>
      <button type="button" class="placeholder-btn" @click="emit('edit')">
        <v-icon size="small">mdi-pencil-outline</v-icon>
        Edit page
      </button>
    </div>

    <div v-else class="carousel">
      <!-- ── Main display ─────────────────────────────── -->
      <div class="carousel-main">

        <!-- Video -->
        <template v-if="current.type === 'video'">
          <iframe
            :key="current.id"
            :src="`https://www.youtube.com/embed/${current.id}`"
            class="carousel-iframe"
            frameborder="0"
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowfullscreen
          />
        </template>

        <!-- Photo -->
        <template v-else>
          <img
            :key="current.url"
            :src="current.url"
            :alt="current.caption || `Photo ${activeIndex}`"
            class="carousel-img"
          />
        </template>

        <!-- Prev arrow -->
        <button
          v-if="activeIndex > 0"
          class="carousel-arrow carousel-arrow--prev"
          type="button"
          aria-label="Previous"
          @click="prev"
        >
          <v-icon color="white" size="22">mdi-chevron-left</v-icon>
        </button>

        <!-- Next arrow -->
        <button
          v-if="activeIndex < items.length - 1"
          class="carousel-arrow carousel-arrow--next"
          type="button"
          aria-label="Next"
          @click="next"
        >
          <v-icon color="white" size="22">mdi-chevron-right</v-icon>
        </button>

        <!-- Thumbnail strip — bottom-left overlay -->
        <div class="thumb-strip">
          <button
            v-for="(item, i) in items"
            :key="i"
            class="thumb-btn"
            :class="{ 'thumb-btn--active': i === activeIndex }"
            type="button"
            :aria-label="`Go to item ${i + 1}`"
            @click="activeIndex = i"
          >
            <img :src="item.thumb" alt="" class="thumb-img" />
            <div v-if="item.type === 'video'" class="thumb-play" aria-hidden="true">
              <v-icon size="12" color="white">mdi-play</v-icon>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Caption and video date below -->
    <p v-if="current && current.caption" class="carousel-caption">{{ current.caption }}</p>
    <p v-if="current && current.type === 'video' && videoDate" class="carousel-date">{{ videoDate }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  yt?: string
  videoDate?: string
  localizedGallery: Array<{ url: string; caption?: string }>
}>()

const emit = defineEmits<{ edit: [] }>()

const { t: $t } = useI18n()
const runtimeConfig = useRuntimeConfig()
const baseURL = (runtimeConfig.app?.baseURL ?? '/').replace(/\/$/, '')

const resolveUrl = (url: string) =>
  url.startsWith('http://') || url.startsWith('https://') || url.startsWith('//')
    ? url
    : `${baseURL}${url.startsWith('/') ? url : `/${url}`}`

type MediaItem =
  | { type: 'video'; id: string; thumb: string; caption?: undefined; url?: undefined }
  | { type: 'photo'; url: string; thumb: string; caption?: string; id?: undefined }

const items = computed<MediaItem[]>(() => {
  const list: MediaItem[] = []
  if (props.yt) {
    list.push({
      type: 'video',
      id: props.yt,
      thumb: `https://img.youtube.com/vi/${props.yt}/mqdefault.jpg`,
    })
  }
  for (const photo of props.localizedGallery ?? []) {
    const url = resolveUrl(photo.url)
    list.push({ type: 'photo', url, thumb: url, caption: photo.caption })
  }
  return list
})

const activeIndex = ref(0)
const current = computed(() => items.value[activeIndex.value])

const prev = () => {
  if (activeIndex.value > 0) activeIndex.value = activeIndex.value - 1
}
const next = () => {
  if (activeIndex.value < items.value.length - 1) activeIndex.value = activeIndex.value + 1
}

const handleKey = (e: KeyboardEvent) => {
  if (e.key === 'ArrowLeft') prev()
  else if (e.key === 'ArrowRight') next()
}
onMounted(() => window.addEventListener('keydown', handleKey))
onBeforeUnmount(() => window.removeEventListener('keydown', handleKey))
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-gallery {
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

/* ── Gallery placeholder ───────────────────────── */
.gallery-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  min-height: 280px;
  padding: 2rem;
  background: rgba(76, 160, 73, 0.05);
  border: 1px dashed rgba(76, 160, 73, 0.3);
  border-radius: 10px;
  text-align: center;

  h3 {
    font-size: 1.125rem;
    font-weight: 600;
    color: $earth-90;
    margin: 0;
  }

  p {
    font-size: 0.875rem;
    color: $text-secondary;
    margin: 0;
  }
}

.placeholder-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: $green-forest;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 10px 16px;
  font-family: $font-family-base;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s ease;

  &:hover {
    background: $green-leaf;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

/* ── Carousel shell ─────────────────────────────── */
.carousel {
  border-radius: 10px;
  overflow: hidden;
  background: #000;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.carousel-main {
  position: relative;
  aspect-ratio: 16/9;
  overflow: hidden;
}

/* ── Media items ────────────────────────────────── */
.carousel-iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

.carousel-img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ── Navigation arrows ──────────────────────────── */
.carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s ease;
  z-index: 2;

  /* Keep arrows above the thumb strip */
  margin-bottom: 68px;

  &:hover {
    background: rgba(0, 0, 0, 0.7);
  }

  &--prev { left: 10px; }
  &--next { right: 10px; }
}

/* ── Thumbnail strip ────────────────────────────── */
.thumb-strip {
  position: absolute;
  bottom: 12px;
  left: 12px;
  right: 12px;
  display: flex;
  gap: 5px;
  justify-content: flex-start;
  padding: 6px 8px;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
  border-radius: 8px;
  overflow-x: auto;
  scrollbar-width: none;
  z-index: 1;

  &::-webkit-scrollbar {
    display: none;
  }
}

.thumb-btn {
  position: relative;
  flex-shrink: 0;
  width: 54px;
  height: 38px;
  border-radius: 5px;
  overflow: hidden;
  border: 2px solid transparent;
  padding: 0;
  cursor: pointer;
  background: $earth-30;
  transition: border-color 0.15s ease, opacity 0.15s ease;
  opacity: 0.65;

  &--active {
    border-color: white;
    opacity: 1;
  }

  &:hover:not(&--active) {
    opacity: 0.9;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

.thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.thumb-play {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.35);
}

/* ── Caption ────────────────────────────────────── */
.carousel-caption {
  margin: $rhythm-1 0 0;
  font-size: 12px;
  color: $text-caption;
  text-align: center;
  min-height: 1.4em;
}

.carousel-date {
  margin: 4px 0 0;
  font-size: 11px;
  color: $text-secondary;
  text-align: center;
  font-weight: 500;
}
</style>
