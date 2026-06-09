<template>
  <div class="research-page">
    <!-- Header -->
    <div class="research-header">
      <div class="header-content">
        <h1>Food Socioscope Research</h1>
        <p class="tagline">What research insights do you need?</p>
        <p class="description">
          Select the research and strategic tools that would be most valuable for your initiative.
          We'll provide additional insights based on your profile.
        </p>
      </div>
    </div>

    <!-- Main Form -->
    <div class="research-container">
      <ResearchForm />
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default',
})

useHead({
  title: 'Food Socioscope Research',
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.research-page {
  min-height: 100vh;
  background: $cream;
}

.research-header {
  background: linear-gradient(135deg, $forest-green 0%, $green-forest 100%);
  color: white;
  padding: 3rem 1.5rem;
  text-align: center;

  @media (max-width: 768px) {
    padding: 2rem 1rem;
  }
}

.header-content {
  max-width: 800px;
  margin: 0 auto;

  h1 {
    font-size: 2.5rem;
    margin: 0 0 0.5rem;
    font-weight: 700;

    @media (max-width: 768px) {
      font-size: 1.75rem;
    }
  }

  .tagline {
    font-size: 1.25rem;
    margin: 0 0 1rem;
    opacity: 0.95;

    @media (max-width: 768px) {
      font-size: 1rem;
    }
  }

  .description {
    font-size: 0.95rem;
    line-height: 1.6;
    margin: 0;
    opacity: 0.9;
  }
}

.research-container {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1rem;

  @media (max-width: 768px) {
    margin: 1rem auto;
  }
}
</style>
