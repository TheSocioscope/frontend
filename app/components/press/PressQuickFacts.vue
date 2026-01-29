<template>
  <section class="section section-beige">
    <div class="container">
      <div class="press-intro">
        <h2>{{ $t('press.quickFacts.title') }}</h2>
        <p>{{ $t('press.quickFacts.description') }}</p>
      </div>

      <div class="quick-facts">
        <div class="fact-card">
          <h3>{{ $t('press.quickFacts.whatWeDo.title') }}</h3>
          <p>{{ $t('press.quickFacts.whatWeDo.content') }}</p>
        </div>

        <div class="fact-card">
          <h3>{{ $t('press.quickFacts.mission.title') }}</h3>
          <p>{{ $t('press.quickFacts.mission.content') }}</p>
        </div>

        <div class="fact-card">
          <h3>{{ $t('press.quickFacts.keyInfo.title') }}</h3>
          <ul>
            <li>{{ $t('press.quickFacts.keyInfo.founded') }}</li>
            <li>{{ $t('press.quickFacts.keyInfo.headquarters') }}</li>
            <li>{{ $t('press.quickFacts.keyInfo.reach') }}</li>
            <li>{{ $t('press.quickFacts.keyInfo.website') }}</li>
          </ul>
        </div>

        <div class="fact-card">
          <h3>{{ $t('press.quickFacts.audience.title') }}</h3>
          <ul>
            <li>{{ $t('press.quickFacts.audience.professionals') }}</li>
            <li>{{ $t('press.quickFacts.audience.researchers') }}</li>
            <li>{{ $t('press.quickFacts.audience.practitioners') }}</li>
            <li>{{ $t('press.quickFacts.audience.policymakers') }}</li>
          </ul>
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

.section {
  padding: 5rem 0;
}

.section-beige {
  background: $warm-beige;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.press-intro {
  max-width: 800px;
  margin: 0 auto 4rem;
  text-align: center;

  h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    font-weight: 700;
  }

  p {
    font-size: 1.15rem;
    line-height: 1.8;
    opacity: 0.85;
  }
}

.quick-facts {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.fact-card {
  background: white;
  padding: 2rem;
  border: 2px solid $warm-beige;
  border-left: 4px solid $green-bright;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(44, 36, 22, 0.1);
  }

  h3 {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    margin-bottom: 1rem;
    color: $forest-green;
    font-weight: 700;
  }

  p {
    font-size: 1.05rem;
    line-height: 1.7;
    margin: 0;
  }

  ul {
    list-style: none;
    padding: 0;
  }

  li {
    padding: 0.5rem 0;
    padding-left: 1.5rem;
    position: relative;

    &:before {
      content: '•';
      position: absolute;
      left: 0;
      color: $green-bright;
      font-weight: bold;
      font-size: 1.2rem;
    }
  }
}

@media (max-width: 1024px) {
  .quick-facts {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .section {
    padding: 4rem 0;
  }
}
</style>
