<template>
  <section class="section stories-section">
    <v-container>
      <div class="section-header text-center">
        <h2 class="section-title">{{ $t('stories.title') }}</h2>
        <p class="section-subtitle">{{ $t('stories.subtitle') }}</p>
      </div>

      <v-row>
        <v-col v-for="(story, index) in displayedStories" :key="index" cols="12" md="4">
          <v-card
            class="story-card h-100"
            elevation="2"
            :to="story._path ? localePath(story._path) : undefined"
          >
            <div class="story-thumbnail">
              <v-img v-if="story.image" :src="story.image" :alt="story.title" cover height="200" />
              <div v-else class="story-placeholder">
                <span class="play-icon">{{ $t('stories.videoPlaceholder') }}</span>
              </div>
            </div>

            <v-card-text>
              <h4 class="mb-2">{{ story.title }}</h4>
              <p>{{ story.description || story.excerpt }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <div v-if="stories && stories.length > 6" class="text-center mt-8">
        <v-btn :to="localePath('/stories')" color="secondary" size="large" variant="elevated">
          View All Stories
        </v-btn>
      </div>
    </v-container>
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
@use '../../assets/styles/variables' as *;

.stories-section {
  background: white;
}

.section-header {
  margin-bottom: $spacing-3xl;
}

.section-subtitle {
  font-size: 1.3rem;
  color: $brown-dark;

  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
}

.story-card {
  background: $surface-cream;
  transition:
    transform $transition-base,
    box-shadow $transition-base;
  overflow: hidden;

  &:hover {
    transform: translateY(-5px);
    box-shadow: $shadow-lg !important;
  }

  h4 {
    font-size: 1.2rem;
    color: $brown-medium;
    font-weight: 500;
  }

  p {
    color: $brown-dark;
    font-size: 0.95rem;
    line-height: 1.5;
  }
}

.story-thumbnail {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.story-placeholder {
  height: 100%;
  background: linear-gradient(135deg, $green-light-olive, $green-olive);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0.8;
}

.play-icon {
  font-size: 3rem;
}
</style>
