<template>
  <section class="hero-section">
    <div class="container">
      <div class="hero-content">
        <div class="hero-text">
          <h1 class="hero-title">
            {{ $t('products.hero.title') }}
          </h1>
          <p class="hero-subtitle">
            {{ $t('products.hero.subtitle') }}
          </p>
        </div>
        <div class="hero-image">
          <div class="hero-animation">
            <div class="floating-element floating-element-1" />
            <div class="floating-element floating-element-2" />
            <div class="floating-element floating-element-3" />
            <div class="floating-element floating-element-4" />
            <div class="cart-container">
              <div class="cart">🛒</div>
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
  width: 100%;
  height: 100%;
  position: relative;
  background: $warm-beige;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-container {
  position: relative;
  z-index: 1;
  animation: bounce 2s ease-in-out infinite;
}

.cart {
  font-size: 6rem;

  @media (max-width: 768px) {
    font-size: 4rem;
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

.floating-element {
  position: absolute;
  border-radius: 50%;
  opacity: 0.12;
  animation: float 6s ease-in-out infinite;
}

.floating-element-1 {
  width: 130px;
  height: 130px;
  background: $green-bright;
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.floating-element-2 {
  width: 95px;
  height: 95px;
  background: $forest-green;
  top: 65%;
  right: 15%;
  animation-delay: 1.5s;
}

.floating-element-3 {
  width: 75px;
  height: 75px;
  background: $green-bright;
  bottom: 20%;
  left: 40%;
  animation-delay: 3s;
}

.floating-element-4 {
  width: 110px;
  height: 110px;
  background: $forest-green;
  top: 35%;
  right: 35%;
  animation-delay: 4.5s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) scale(1);
  }
  50% {
    transform: translateY(-25px) scale(1.08);
  }
}
</style>
