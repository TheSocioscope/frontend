<template>
  <section class="section press-contact">
    <div class="container">
      <div class="press-contact-content">
        <h2>{{ $t('press.contact.title') }}</h2>
        <p>{{ $t('press.contact.description') }}</p>

        <div class="contact-info">
          <div class="contact-item">
            <div class="contact-icon">📧</div>
            <a href="mailto:info@thesocioscope.org">info@thesocioscope.org</a>
          </div>
          <div class="contact-item">
            <div class="contact-icon">🌐</div>
            <a href="https://thesocioscope.org" target="_blank">thesocioscope.org</a>
          </div>
        </div>

        <div class="contact-action">
          <NuxtLink :to="localePath('/contact')" class="btn btn-primary">
            {{ $t('press.contact.button') }}
          </NuxtLink>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const localePath = useLocalePath()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section {
  padding: 5rem 0;
}

.press-contact {
  background: $warm-beige;
  text-align: center;
  border-top: 3px solid $green-bright;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.press-contact-content {
  max-width: 700px;
  margin: 0 auto;

  h2 {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    margin-bottom: 1.5rem;
    font-weight: 700;
  }

  p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    line-height: 1.7;
  }
}

.contact-info {
  display: flex;
  justify-content: center;
  gap: 3rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
}

.contact-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.contact-icon {
  font-size: 2rem;
}

.contact-item a {
  color: $green-bright;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: color 0.3s;

  &:hover {
    color: $forest-green;
  }
}

.contact-action {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  font-weight: 600;
  text-decoration: none;
  font-family: 'Playfair Display', serif;
  font-size: 1rem;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  cursor: pointer;
}

.btn-primary {
  background: $green-bright;
  color: white;
  border-color: $green-bright;

  &:hover {
    background: $forest-green;
    border-color: $forest-green;
  }
}

@media (max-width: 768px) {
  .section {
    padding: 4rem 0;
  }

  .contact-info {
    flex-direction: column;
    gap: 1.5rem;
  }
}
</style>
