<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            {{ title }}
          </h1>
          <p class="hero-subtitle">
            {{ subtitle }}
          </p>
          <slot name="cta" />
        </div>
        <div class="hero-image">
          <div class="hero-animation">
            <div class="floating-element floating-element-1" />
            <div class="floating-element floating-element-2" />
            <div class="floating-element floating-element-3" />
            <div v-if="icon" class="icon-container">
              <div class="icon">{{ icon }}</div>
            </div>
            <slot name="custom-icon" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  subtitle: string
  icon?: string
}>()
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
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.floating-element-2 {
  width: 80px;
  height: 80px;
  background: $brown-dark;
  top: 60%;
  right: 15%;
  animation-delay: 1s;
}

.floating-element-3 {
  width: 100px;
  height: 100px;
  background: $green-bright;
  bottom: 20%;
  left: 20%;
  animation-delay: 2s;
}

.icon-container {
  position: relative;
  z-index: 1;
}

.icon {
  font-size: 6rem;
  animation: bounce 3s ease-in-out infinite;

  @media (max-width: 768px) {
    font-size: 4rem;
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) translateX(0);
  }
  25% {
    transform: translateY(-20px) translateX(10px);
  }
  50% {
    transform: translateY(-10px) translateX(-10px);
  }
  75% {
    transform: translateY(-25px) translateX(5px);
  }
}

@keyframes bounce {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}
</style>
