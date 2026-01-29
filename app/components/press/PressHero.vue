<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">{{ $t('press.hero.title') }}</h1>
          <p class="hero-subtitle">{{ $t('press.hero.subtitle') }}</p>
        </div>
        <div class="hero-image">
          <div class="hero-animation">
            <div class="floating-element floating-element-1" />
            <div class="floating-element floating-element-2" />
            <div class="floating-element floating-element-3" />
            <div class="photo-placeholder">📰</div>
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
@use '~~/assets/styles/variables' as *;

.hero-section {
  background: $warm-beige;
  padding: 0;
  position: relative;
  overflow: hidden;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  min-height: 400px;
}

.hero-text {
  padding: 4rem 3rem 4rem 0;
}

.hero-title {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  margin-bottom: 1rem;
  line-height: 1.2;
  color: $brown-dark;
  font-weight: 700;
}

.hero-subtitle {
  font-size: clamp(1.1rem, 2vw, 1.4rem);
  line-height: 1.5;
  color: $brown-dark;
  font-weight: 400;
  opacity: 0.85;
}

.hero-image {
  height: 100%;
  min-height: 400px;
  position: relative;
  background: $cream;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-animation {
  width: 100%;
  height: 100%;
  position: relative;
  background: $warm-beige;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-element {
  position: absolute;
  border-radius: 50%;
  opacity: 0.12;
  animation: float 6s ease-in-out infinite;
}

.floating-element-1 {
  width: 120px;
  height: 120px;
  background: $green-bright;
  top: 15%;
  left: 15%;
  animation-delay: 0s;
}

.floating-element-2 {
  width: 90px;
  height: 90px;
  background: $forest-green;
  top: 55%;
  right: 20%;
  animation-delay: 1.5s;
}

.floating-element-3 {
  width: 70px;
  height: 70px;
  background: $green-bright;
  bottom: 25%;
  left: 35%;
  animation-delay: 3s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-25px) scale(1.1);
  }
}

.photo-placeholder {
  font-size: 5rem;
  opacity: 0.3;
  position: relative;
  z-index: 1;
}

@media (max-width: 768px) {
  .hero-content {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .hero-text {
    padding: 3rem 0 2rem;
    text-align: center;
  }

  .hero-image {
    min-height: 300px;
  }

  .hero-title {
    font-size: 2rem;
  }

  .hero-subtitle {
    font-size: 1.1rem;
  }
}
</style>
