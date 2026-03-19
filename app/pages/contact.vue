<template>
  <div>
    <PageHero :title="$t('contact.hero.title')" :subtitle="$t('contact.hero.subtitle')" icon="mdi-email-outline" />
    <section class="section">
      <div class="container">
        <div class="contact-grid">
          <div class="contact-main">
            <h2>{{ $t('contact.form.title') }}</h2>
            <p>{{ $t('contact.hero.subtitle') }}</p>
            <a href="mailto:contact@thesocioscope.org" class="mailto-btn">
              contact@thesocioscope.org
            </a>
          </div>
          <ContactInfo />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

useHead({
  title: $t('contact.meta.title'),
  meta: [
    {
      name: 'description',
      content: $t('contact.meta.description')
    }
  ]
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section {
  padding: 5rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: start;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
}

.contact-main {
  h2 {
    font-family: $font-family-display;
    font-size: 2rem;
    font-weight: $font-weight-bold;
    color: $brown-dark;
    margin-bottom: 1rem;
  }

  p {
    font-size: 1.1rem;
    line-height: 1.7;
    color: $brown-dark;
    opacity: 0.85;
    margin-bottom: 2rem;
  }
}

.mailto-btn {
  display: inline-block;
  padding: 1rem 2rem;
  background: $green-bright;
  color: white;
  text-decoration: none;
  font-weight: $font-weight-semibold;
  font-size: 1.05rem;
  transition: background 0.3s;

  &:hover {
    background: $forest-green;
  }
}
</style>
