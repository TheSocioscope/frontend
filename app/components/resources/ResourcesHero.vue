<template>
  <section class="hero">
    <div class="container">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">{{ $t('resources.hero.title') }}</h1>
          <p class="hero-subtitle">{{ $t('resources.hero.subtitle') }}</p>
          <div class="hero-cta">
            <a href="#resources" class="btn">{{ $t('resources.hero.browseCta') }}</a>
            <button class="btn btn-secondary" @click="$emit('submit')">
              {{ $t('resources.hero.submitCta') }}
            </button>
          </div>
        </div>
        <div class="hero-image">
          <div class="hero-animation">
            <div class="resource-icon">📚</div>
            <div class="floating-element floating-element-1" />
            <div class="floating-element floating-element-2" />
            <div class="floating-element floating-element-3" />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineEmits<{
  submit: []
}>()
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.hero {
  background: linear-gradient(135deg, $cream 0%, $warm-beige 100%);
  padding: 8rem 0 6rem;
  position: relative;
  overflow: hidden;

  @media (max-width: 768px) {
    padding: 6rem 0 4rem;
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero-content {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;

  @media (max-width: 968px) {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
}

.hero-text {
  max-width: 600px;
}

.hero-title {
  font-family: $font-family-display;
  font-size: 4rem;
  font-weight: 700;
  color: $brown-dark;
  margin-bottom: 1.5rem;
  line-height: 1.1;

  @media (max-width: 768px) {
    font-size: 3rem;
  }
}

.hero-subtitle {
  font-size: 1.25rem;
  color: $brown-dark;
  opacity: 0.8;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.hero-cta {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.btn {
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 0;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;
  background: $green-bright;
  color: white;
  border: none;
  cursor: pointer;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }
}

.btn-secondary {
  background: transparent;
  color: $brown-dark;
  border: 2px solid $brown-dark;

  &:hover {
    background: $brown-dark;
    color: white;
  }
}

.hero-image {
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  min-height: 400px;

  @media (max-width: 968px) {
    min-height: 300px;
  }
}

.hero-animation {
  position: relative;
  width: 300px;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.resource-icon {
  font-size: 8rem;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-20px);
  }
}

.floating-element {
  position: absolute;
  background: $green-bright;
  opacity: 0.2;
  border-radius: 50%;
  animation: floatCircle 4s ease-in-out infinite;
}

.floating-element-1 {
  width: 80px;
  height: 80px;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.floating-element-2 {
  width: 60px;
  height: 60px;
  top: 60%;
  right: 15%;
  animation-delay: 1s;
}

.floating-element-3 {
  width: 100px;
  height: 100px;
  bottom: 10%;
  left: 20%;
  animation-delay: 2s;
}

@keyframes floatCircle {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-15px) scale(1.1);
  }
}
</style>
