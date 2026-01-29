<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            {{ $t('about.hero.title') }}
          </h1>
          <p class="hero-subtitle">
            {{ $t('about.hero.subtitle') }}
          </p>
        </div>
        <div class="hero-image">
          <div class="hero-animation">
            <div class="floating-element floating-element-1" />
            <div class="floating-element floating-element-2" />
            <div class="floating-element floating-element-3" />
            <div class="floating-element floating-element-4" />
            <div class="photo-placeholder">🌿</div>
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
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  align-items: center;
  min-height: 500px;

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
  font-size: clamp(2rem, 4vw, 3rem);
  margin-bottom: 1rem;
  line-height: 1.2;
  color: $brown-dark;
  font-weight: $font-weight-bold;
  text-transform: uppercase;
  letter-spacing: 0.02em;
  font-family: $font-family-display;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 2.5vw, 1.8rem);
  line-height: 1.4;
  color: $brown-dark;
  font-weight: $font-weight-regular;
  opacity: 0.85;
  font-family: $font-family-display;
}

.hero-image {
  height: 100%;
  min-height: 500px;
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
  width: 100%;
  height: 100%;
  position: relative;
  background: linear-gradient(135deg, $warm-beige 0%, $cream 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-element {
  position: absolute;
  border-radius: 50%;
  opacity: 0.15;
  animation: float 6s ease-in-out infinite;
}

.floating-element-1 {
  width: 150px;
  height: 150px;
  background: $green-bright;
  top: 20%;
  left: 20%;
  animation-delay: 0s;
}

.floating-element-2 {
  width: 100px;
  height: 100px;
  background: $forest-green;
  top: 60%;
  right: 25%;
  animation-delay: 1s;
}

.floating-element-3 {
  width: 80px;
  height: 80px;
  background: $green-bright;
  bottom: 30%;
  left: 40%;
  animation-delay: 2s;
}

.floating-element-4 {
  width: 120px;
  height: 120px;
  background: $forest-green;
  top: 40%;
  right: 15%;
  animation-delay: 3s;
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

.photo-placeholder {
  font-size: 4rem;
  opacity: 0.3;
  position: relative;
  z-index: 1;
}
</style>
