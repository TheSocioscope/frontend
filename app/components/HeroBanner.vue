<template>
  <section class="hero-section">
    <!-- Video Background -->
    <div class="video-container">
      <video
        v-if="videoLoaded"
        autoplay
        muted
        loop
        playsinline
        class="hero-video"
        @loadeddata="onVideoLoaded"
      >
        <source src="https://thesocioscope.org/thesocioscope/splash.webm" type="video/webm" />
      </video>

      <!-- Placeholder while video loads -->
      <div v-if="!videoLoaded" class="video-placeholder">
        <v-progress-circular indeterminate color="white" size="64" />
      </div>
    </div>

    <!-- Overlay Content -->
    <v-container class="hero-overlay">
      <v-row justify="center">
        <v-col cols="12" class="text-center">
          <h1 class="hero-title text-shadow letter-spacing-wide">
            {{ $t('hero.title') }}
          </h1>
          <p class="hero-subtitle text-shadow">
            {{ $t('hero.subtitle') }}
          </p>
          <p class="hero-tagline">
            {{ $t('hero.tagline') }}
          </p>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const videoLoaded = ref(false)

const onVideoLoaded = () => {
  videoLoaded.value = true
}

// Preload video
onMounted(() => {
  videoLoaded.value = true
})
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.hero-section {
  position: relative;
  height: 80vh;
  min-height: 600px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  background: $brown-dark;
}

.video-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;

  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.4);
    z-index: 1;
  }
}

.hero-video {
  position: absolute;
  top: 50%;
  left: 50%;
  min-width: 100%;
  min-height: 100%;
  width: auto;
  height: auto;
  transform: translate(-50%, -50%);
  object-fit: cover;
}

.video-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, $surface-cream 0%, $cream-light 100%);
}

.hero-overlay {
  position: relative;
  z-index: 2;
  color: white;
  text-align: center;
  padding: $spacing-xl;
}

.hero-title {
  color: #ffffff;
  font-size: 4rem;
  font-weight: 300;
  letter-spacing: 2px;
  margin-bottom: $spacing-lg;

  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
}

.hero-subtitle {
  font-size: 1.8rem;
  font-weight: 300;
  margin-bottom: $spacing-md;
  opacity: 0.95;

  @media (max-width: 768px) {
    font-size: 1.4rem;
  }
}

.hero-tagline {
  font-size: 1.2rem;
  opacity: 0.9;
  max-width: 700px;
  margin: 0 auto;

  @media (max-width: 768px) {
    font-size: 1rem;
  }
}
</style>
