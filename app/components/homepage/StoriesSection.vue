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
          @click="story._path && navigateTo(localePath(story._path))"
        >
          <div class="story-thumbnail">
            <img v-if="story.image" :src="story.image" :alt="story.title" class="story-image" />
            <span v-else class="play-icon">{{ $t('stories.videoPlaceholder') }}</span>
          </div>
          <div class="story-content">
            <h4>{{ story.title }}</h4>
            <p>{{ story.description || story.excerpt }}</p>
          </div>
        </div>
      </div>

      <div v-if="stories && stories.length > 6" class="text-center mt-8">
        <NuxtLink :to="localePath('/stories')" class="btn btn-outline"> View All Stories </NuxtLink>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t, locale } = useI18n()
const localePath = useLocalePath()

// Fallback stories from i18n
const fallbackStories = [
  {
    title: $t('stories.video1.title'),
    description: $t('stories.video1.description')
  },
  {
    title: $t('stories.video2.title'),
    description: $t('stories.video2.description')
  },
  {
    title: $t('stories.video3.title'),
    description: $t('stories.video3.description')
  },
  {
    title: $t('stories.video4.title'),
    description: $t('stories.video4.description')
  },
  {
    title: $t('stories.video5.title'),
    description: $t('stories.video5.description')
  },
  {
    title: $t('stories.video6.title'),
    description: $t('stories.video6.description')
  }
]

// Fetch stories from content
const { data: stories } = await useAsyncData(
  'stories',
  async () => {
    try {
      const content = await queryContent(`stories/${locale.value}`)
        .where({ published: true })
        .sort({ publishedAt: -1 })
        .limit(6)
        .find()
      return content
    } catch (e) {
      return null
    }
  },
  { watch: [locale], default: () => null }
)

const displayedStories = computed(() => {
  return stories.value && stories.value.length > 0 ? stories.value : fallbackStories
})
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
  width: 100%;
  height: 200px;
  background: $green-bright;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 3rem;
  overflow: hidden;
}

.story-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-icon {
  font-size: 3rem;
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
