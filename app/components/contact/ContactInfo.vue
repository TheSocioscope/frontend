<template>
  <div class="contact-info">
    <div class="info-card">
      <div class="info-icon">📧</div>
      <h3>{{ $t('contact.info.email.title') }}</h3>
      <p>
        <a href="mailto:info@socioscope.org">{{ $t('contact.info.email.address') }}</a>
      </p>
    </div>

    <div class="info-card">
      <div class="info-icon">📍</div>
      <h3>{{ $t('contact.info.location.title') }}</h3>
      <p class="address">{{ $t('contact.info.location.address') }}</p>
    </div>

    <div class="info-card">
      <div class="info-icon">🌐</div>
      <h3>{{ $t('contact.info.social.title') }}</h3>
      <div class="social-links">
        <a
          href="https://twitter.com/socioscope"
          target="_blank"
          rel="noopener noreferrer"
          :title="$t('contact.info.social.twitter')"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"
            />
          </svg>
        </a>
        <a
          href="https://linkedin.com/company/socioscope"
          target="_blank"
          rel="noopener noreferrer"
          :title="$t('contact.info.social.linkedin')"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"
            />
          </svg>
        </a>
        <a
          href="https://youtube.com/@socioscope"
          target="_blank"
          rel="noopener noreferrer"
          :title="$t('contact.info.social.youtube')"
        >
          <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path
              d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"
            />
          </svg>
        </a>
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

.info-card {
  background: $warm-beige;
  padding: 2rem;
  border-left: 4px solid $green-bright;
  transition: all 0.3s ease;

  &:hover {
    transform: translateX(5px);
    box-shadow: 0 8px 20px rgba(44, 36, 22, 0.1);
  }
}

.info-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.info-card h3 {
  font-family: 'Playfair Display', serif;
  font-size: 1.4rem;
  margin-bottom: 0.75rem;
  font-weight: 700;
}

.info-card p {
  margin: 0;
  line-height: 1.7;
  font-size: 1.05rem;
}

.address {
  white-space: pre-line;
}

.info-card a {
  color: $green-bright;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s;

  &:hover {
    color: $forest-green;
  }
}

.social-links {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;

  a {
    width: 45px;
    height: 45px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: white;
    color: $brown-dark;
    border: 2px solid $warm-beige;
    transition: all 0.3s;

    &:hover {
      background: $green-bright;
      color: white;
      border-color: $green-bright;
      transform: translateY(-3px);
    }
  }
}
</style>
