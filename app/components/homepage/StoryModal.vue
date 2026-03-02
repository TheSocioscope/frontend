<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="story" class="modal-overlay" @click="emit('close')">
        <div class="modal-content" @click.stop>
          <button class="close-btn" @click="emit('close')">&times;</button>

          <!-- Video embed -->
          <div v-if="story.video" class="video-wrapper">
            <iframe
              :src="`https://www.youtube-nocookie.com/embed/${story.video}?autoplay=1`"
              :title="story.title"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowfullscreen
            />
          </div>

          <div class="modal-body">
            <div class="text overline">{{ formatDate(story.publishedAt) }}</div>
            <h2>{{ story.title }}</h2>
            <ContentRenderer v-if="story.body" :value="story" class="prose" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
interface Story {
  title: string
  description?: string
  video?: string
  body?: object
  [key: string]: unknown
}
const formatDate = (date) => {
  if (!date) return ''
  try {
    return new Date(date).toLocaleDateString()
  } catch {
    return date
  }
}
defineProps<{
  story: Story | null
}>()

const emit = defineEmits<{
  close: []
}>()

// Close on Escape key
onMounted(() => {
  const onKey = (e: KeyboardEvent) => e.key === 'Escape' && emit('close')
  window.addEventListener('keydown', onKey)
  onUnmounted(() => window.removeEventListener('keydown', onKey))
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: $z-modal;
  padding: 1rem;
}

.modal-content {
  position: relative;
  background: white;
  border-radius: $border-radius-lg;
  width: 100%;
  max-width: 760px;
  max-height: 90vh;
  overflow-y: auto;
}

.close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  z-index: 1;
  background: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  border-radius: 50%;
  width: 36px;
  height: 36px;
  font-size: 1.4rem;
  line-height: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background $transition-base;

  &:hover {
    background: rgba(0, 0, 0, 0.65);
  }
}

.video-wrapper {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  background: #000;
  border-radius: $border-radius-lg $border-radius-lg 0 0;
  overflow: hidden;

  iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: none;
  }
}

.modal-body {
  padding: 2rem;

  h2 {
    font-family: $font-family-display;
    font-size: 1.75rem;
    font-weight: $font-weight-bold;
    color: $brown-dark;
    margin: 0 0 1rem;
  }
}

.description {
  font-size: 1rem;
  color: $brown-medium;
  line-height: 1.7;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.prose {
  font-size: 1rem;
  color: $brown-dark;
  line-height: 1.8;

  :deep(p) {
    margin-bottom: 1rem;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.25s ease;

  .modal-content {
    transition: transform 0.25s ease;
  }
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;

  .modal-content {
    transform: translateY(12px);
  }
}
</style>
