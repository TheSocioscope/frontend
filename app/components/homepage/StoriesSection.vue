<template>
  <section class="stories">
    <div class="container">
      <div class="section-header">
        <h2>{{ $t('stories.title') }}</h2>
      </div>

      <div class="stories-grid">
        <div
          v-for="(story, index) in displayedStories"
          :key="index"
          class="story-card"
          @click="openStory(story)"
        >
          <div class="story-thumbnail">
            <img
              v-if="story.video"
              :src="`https://img.youtube.com/vi/${story.video}/hqdefault.jpg`"
              :alt="story.title"
              class="story-image"
            />
            <img
              v-else-if="story.image"
              :src="story.image"
              :alt="story.title"
              class="story-image"
            />
            <span v-else class="thumbnail-placeholder" />
            <span v-if="story.video" class="play-icon" aria-hidden="true">&#9654;</span>
          </div>
          <div class="story-content">
            <h4>{{ story.title }}</h4>
            <p>{{ story.description || story.excerpt }}</p>
          </div>
        </div>
      </div>

      <HomepageStoryModal :story="activeStory" @close="activeStory = null" />

      <div v-if="stories && stories.length > 6" class="text-center mt-8">
        <NuxtLink :to="localePath('/stories')" class="btn btn-outline"> View All Stories </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
interface Story {
  title: string
  description?: string
  excerpt?: string
  image?: string
  video?: string
  body?: object
  _path?: string
  [key: string]: unknown
}

const { t: $t } = useI18n()
const localePath = useLocalePath()

const { allItems: stories } = useLocalizedCollection<Story>('stories', {
  sortBy: 'publishedAt',
  sortOrder: 'desc'
})

const displayedStories = computed(() => stories.value.slice(0, 6))

const activeStory = ref<Story | null>(null)

const openStory = (story: Story) => {
  activeStory.value = story
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.stories {
  padding: 6rem 0;
  background: $cream;
}

.stories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;

  @media (max-width: 968px) {
    grid-template-columns: 1fr;
  }
}

.story-card {
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition:
    transform 0.3s,
    box-shadow 0.3s;
  cursor: pointer;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
  }
}

.story-thumbnail {
  position: relative;
  width: 100%;
  height: 200px;
  background: $green-bright;
  overflow: hidden;
}

.story-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumbnail-placeholder {
  display: block;
  width: 100%;
  height: 100%;
  background: $green-bright;
}

.play-icon {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  background: rgba(0, 0, 0, 0.25);
  transition: background 0.3s;

  .story-card:hover & {
    background: rgba(0, 0, 0, 0.45);
  }
}

.story-content {
  padding: 1.5rem;

  h4 {
    font-family: $font-family-display;
    font-size: 1.5rem;
    font-weight: $font-weight-bold;
    margin-bottom: 0.5rem;
    color: $brown-dark;
  }

  p {
    font-size: 0.95rem;
    color: #666;
    line-height: 1.6;
    margin: 0;
  }
}

.btn {
  display: inline-block;
  padding: 1rem 2.5rem;
  text-decoration: none;
  font-weight: $font-weight-semibold;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  border: none;
  cursor: pointer;
}

.btn-outline {
  background: transparent;
  color: $brown-dark;
  border: 2px solid $brown-dark;

  &:hover {
    background: $brown-dark;
    color: $cream;
  }
}

.text-center {
  text-align: center;
}

.mt-8 {
  margin-top: 3rem;
}
</style>
