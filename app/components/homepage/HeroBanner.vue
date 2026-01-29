<template>
  <section class="hero">
    <!-- Animated Circles Background -->
    <div class="hero-circles">
      <div class="circle circle-1" />
      <div class="circle circle-2" />
      <div class="circle circle-3" />
    </div>

    <!-- Hero Content -->
    <div class="container">
      <div class="hero-content">
        <h1 class="hero-title">{{ $t('hero.title') }}</h1>
        <p class="hero-subtitle">{{ $t('hero.subtitle') }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.hero {
  padding: 8rem 0 6rem;
  background: linear-gradient(135deg, $cream 0%, $warm-beige 100%);
  position: relative;
  overflow: hidden;
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero-content {
  text-align: center;
  position: relative;
  z-index: 2;
}

.hero-title {
  font-family: $font-family-display;
  font-size: $font-size-hero-large;
  font-weight: $font-weight-bold;
  color: $brown-dark;
  margin-bottom: 1.5rem;
  animation: fadeInUp 0.8s ease forwards;
  letter-spacing: 0.05em;
}

.hero-subtitle {
  font-family: $font-family-base;
  font-size: clamp(1.1rem, 2vw, 1.5rem);
  line-height: 1.6;
  font-weight: $font-weight-regular;
  color: $brown-dark;
  opacity: 0;
  animation: fadeInUp 0.8s ease 0.2s forwards;
}

.hero-circles {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.circle {
  position: absolute;
  border-radius: 50%;
  border: 2px solid;
  opacity: 0.3;

  &-1 {
    width: 350px;
    height: 350px;
    border-color: $green-bright;
    animation: pulse 3s ease-in-out infinite;
  }

  &-2 {
    width: 500px;
    height: 500px;
    border-color: $forest-green;
    animation: pulse 3s ease-in-out 1s infinite;
  }

  &-3 {
    width: 650px;
    height: 650px;
    border-color: $brown-dark;
    animation: pulse 3s ease-in-out 2s infinite;
  }
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.5;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 968px) {
  .hero {
    padding: 4rem 0 3rem;
    min-height: 60vh;
  }

  .hero-title {
    font-size: clamp(2.5rem, 8vw, 3.5rem);
  }

  .circle {
    &-1 {
      width: 250px;
      height: 250px;
    }
    &-2 {
      width: 350px;
      height: 350px;
    }
    &-3 {
      width: 450px;
      height: 450px;
    }
  }
}
</style>
