<template>
  <div>
    <PageHero
      :title="$t('contact.hero.title')"
      :subtitle="$t('contact.hero.subtitle')"
      icon="mdi-email-outline"
    />

    <section class="section">
      <div class="container">
        <div class="contact-wrapper">

          <!-- Primary email CTA -->
          <div class="email-block">
            <p class="email-label">{{ $t('contact.info.email.title') }}</p>
            <a href="mailto:info@thesocioscope.org" class="email-link">
              info@thesocioscope.org
            </a>
          </div>

          <div class="divider" />

          <!-- Info row -->
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
  meta: [{ name: 'description', content: $t('contact.meta.description') }]
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section {
  padding: 6rem 0;
  background: $cream;
}

.container {
  max-width: 760px;
  margin: 0 auto;
  padding: 0 2rem;
}

.contact-wrapper {
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.email-block {
  text-align: center;
}

.email-label {
  font-family: $font-family-display;
  font-size: 0.85rem;
  font-weight: $font-weight-semibold;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: $brown-dark;
  opacity: 0.6;
  margin-bottom: 0.75rem;
}

.email-link {
  display: inline-block;
  font-family: $font-family-display;
  font-size: clamp(1.4rem, 3vw, 2rem);
  font-weight: $font-weight-bold;
  color: $green-bright;
  text-decoration: none;
  border-bottom: 2px solid transparent;
  transition: border-color 0.3s, color 0.3s;

  &:hover {
    color: $forest-green;
    border-bottom-color: $forest-green;
  }
}

.divider {
  height: 1px;
  background: $warm-beige;
}
</style>
