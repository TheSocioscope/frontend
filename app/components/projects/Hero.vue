<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            {{ $t('projects.hero.title') }}
          </h1>
          <p class="hero-subtitle">
            {{ $t('projects.hero.subtitle') }}
          </p>
        </div>
        <div class="hero-image">
          <div class="hero-animation">
            <div class="floating-element floating-element-1" />
            <div class="floating-element floating-element-2" />
            <div class="floating-element floating-element-3" />
            <div class="floating-element floating-element-4" />
            <div class="map-container">
              <div class="map-icon">🗺️</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.hero-section {
  background: $warm-beige;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  min-height: 450px;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    min-height: auto;
  }
}

.hero-text {
  padding: 4rem 3rem 4rem 0;

  @media (max-width: 768px) {
    padding: 3rem 0 2rem;
    text-align: center;
  }
}

.hero-title {
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  margin-bottom: 1rem;
  line-height: 1.2;
  color: $brown-dark;
  font-weight: $font-weight-bold;
  font-family: $font-family-display;
}

.hero-subtitle {
  font-size: clamp(1.1rem, 2vw, 1.4rem);
  line-height: 1.5;
  color: $brown-dark;
  font-weight: $font-weight-regular;
  opacity: 0.85;
  font-family: $font-family-display;
}

.hero-image {
  height: 100%;
  min-height: 450px;
  position: relative;
  background: $cream;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;

  @media (max-width: 768px) {
    min-height: 300px;
  }
}

.hero-animation {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-element {
  position: absolute;
  background: $green-bright;
  opacity: 0.15;
  border-radius: 50%;
  animation: float 6s ease-in-out infinite;

  &-1 {
    width: 120px;
    height: 120px;
    top: 15%;
    left: 10%;
    animation-delay: 0s;
  }

  &-2 {
    width: 80px;
    height: 80px;
    top: 60%;
    right: 20%;
    animation-delay: 2s;
  }

  &-3 {
    width: 100px;
    height: 100px;
    bottom: 20%;
    left: 25%;
    animation-delay: 4s;
  }

  &-4 {
    width: 60px;
    height: 60px;
    top: 30%;
    right: 15%;
    animation-delay: 1s;
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-20px) scale(1.05);
  }
}

.map-container {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-icon {
  font-size: 8rem;
  animation: pulse 3s ease-in-out infinite;

  @media (max-width: 768px) {
    font-size: 6rem;
  }
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.9;
  }
}
</style>
