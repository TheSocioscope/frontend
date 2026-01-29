<template>
  <section class="hero">
    <div class="floating-shapes">
      <div class="float-shape float-shape-1" />
      <div class="float-shape float-shape-2" />
      <div class="float-shape float-shape-3" />
    </div>
    <div class="hero-content">
      <div class="container">
        <h1>{{ $t('team.hero.title') }}</h1>
        <p>{{ $t('team.hero.subtitle') }}</p>
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
  background: $warm-beige;
  padding: 6rem 0 4rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background:
    radial-gradient(circle at 20% 50%, rgba(76, 160, 73, 0.08) 0%, transparent 25%),
    radial-gradient(circle at 80% 50%, rgba(39, 66, 29, 0.08) 0%, transparent 25%),
    radial-gradient(circle at 40% 80%, rgba(76, 160, 73, 0.05) 0%, transparent 25%);
  animation: heroRotate 30s linear infinite;
}

@keyframes heroRotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.hero-content {
  position: relative;
  z-index: 1;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.hero h1 {
  font-family: 'Playfair Display', serif;
  font-size: clamp(2.5rem, 5vw, 4rem);
  margin-bottom: 1rem;
  font-weight: 700;
  animation: fadeInUp 0.8s ease;
}

.hero p {
  font-size: 1.25rem;
  max-width: 800px;
  margin: 0 auto;
  opacity: 0.9;
  animation: fadeInUp 0.8s ease 0.2s both;
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

.floating-shapes {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.float-shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.1;
}

.float-shape-1 {
  width: 100px;
  height: 100px;
  background: $green-bright;
  top: 20%;
  left: 10%;
  animation: float1 8s ease-in-out infinite;
}

.float-shape-2 {
  width: 60px;
  height: 60px;
  background: $forest-green;
  top: 60%;
  right: 15%;
  animation: float2 10s ease-in-out infinite;
}

.float-shape-3 {
  width: 80px;
  height: 80px;
  background: $green-bright;
  bottom: 20%;
  left: 30%;
  animation: float3 12s ease-in-out infinite;
}

@keyframes float1 {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(30px, -30px) scale(1.1);
  }
}

@keyframes float2 {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(-40px, 40px) scale(1.2);
  }
}

@keyframes float3 {
  0%,
  100% {
    transform: translate(0, 0) scale(1);
  }
  50% {
    transform: translate(20px, 30px) scale(0.9);
  }
}
</style>
