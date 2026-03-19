<template>
  <div class="contact-info">
    <div class="info-item">
      <v-icon class="info-icon" aria-hidden="true">mdi-email-outline</v-icon>
      <div>
        <h3>{{ $t('contact.info.email.title') }}</h3>
        <a href="mailto:info@thesocioscope.org">info@thesocioscope.org</a>
      </div>
    </div>

    <div class="info-item">
      <v-icon class="info-icon" aria-hidden="true">mdi-map-marker-outline</v-icon>
      <div>
        <h3>{{ $t('contact.info.location.title') }}</h3>
        <p class="address">{{ $t('contact.info.location.address') }}</p>
      </div>
    </div>

    <div class="info-item">
      <v-icon class="info-icon" aria-hidden="true">mdi-share-variant-outline</v-icon>
      <div>
        <h3>{{ $t('contact.info.social.title') }}</h3>
        <div class="social-links">
          <a
            href="https://www.linkedin.com/company/the-socioscope"
            target="_blank"
            rel="noopener noreferrer"
            :aria-label="$t('contact.info.social.linkedin')"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" />
            </svg>
          </a>
          <a
            href="https://www.youtube.com/@thesocioscope"
            target="_blank"
            rel="noopener noreferrer"
            :aria-label="$t('contact.info.social.youtube')"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 1.25rem;
}

.info-icon {
  color: $green-bright;
  font-size: 1.5rem !important;
  flex-shrink: 0;
  margin-top: 0.2rem;
}

.info-item h3 {
  font-family: $font-family-display;
  font-size: 1rem;
  font-weight: $font-weight-semibold;
  color: $brown-dark;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.4rem;
}

.info-item a {
  color: $green-bright;
  text-decoration: none;
  font-size: 1.05rem;
  font-weight: $font-weight-medium;
  transition: color 0.3s;

  &:hover {
    color: $forest-green;
  }
}

.info-item p {
  margin: 0;
  color: $brown-dark;
  font-size: 1rem;
  line-height: 1.6;
  opacity: 0.8;
}

.address {
  white-space: pre-line;
}

.social-links {
  display: flex;
  gap: 0.75rem;
  margin-top: 0.5rem;

  a {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1.5px solid $warm-beige;
    color: $brown-dark;
    transition: all 0.3s;

    &:hover {
      background: $green-bright;
      color: white;
      border-color: $green-bright;
    }
  }
}
</style>
