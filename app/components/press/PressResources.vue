<template>
  <section class="section section-white">
    <div class="container">
      <div class="press-intro">
        <h2>{{ $t('press.resources.title') }}</h2>
        <p>{{ $t('press.resources.description') }}</p>
      </div>

      <div class="media-kit-section">
        <div class="media-kit-card">
          <div class="media-kit-header">
            <div class="media-kit-icon">📄</div>
            <div class="media-kit-info">
              <h3>{{ $t('press.mediaKit.title') }}</h3>
              <p>{{ $t('press.mediaKit.description') }}</p>
            </div>
          </div>

          <div class="media-kit-preview">
            <img
              src="#"
              alt="Socioscope Media Kit Preview"
              style="max-height: 400px; object-fit: contain; margin: 0 auto; display: block"
            />
          </div>

          <div class="media-kit-stats">
            <div class="stat-item">
              <div class="stat-number">{{ $t('press.mediaKit.stats.countries') }}</div>
              <div class="stat-label">{{ $t('press.mediaKit.stats.countriesLabel') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ $t('press.mediaKit.stats.initiatives') }}</div>
              <div class="stat-label">{{ $t('press.mediaKit.stats.initiativesLabel') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ $t('press.mediaKit.stats.interviewers') }}</div>
              <div class="stat-label">{{ $t('press.mediaKit.stats.interviewersLabel') }}</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ $t('press.mediaKit.stats.languages') }}</div>
              <div class="stat-label">{{ $t('press.mediaKit.stats.languagesLabel') }}</div>
            </div>
          </div>

          <div class="media-kit-actions">
            <a href="#" class="btn btn-primary" download>
              <span>⬇</span> {{ $t('press.mediaKit.downloadPdf') }}
            </a>
            <button class="btn btn-outline" @click="shareMediaKit">
              <span>🔗</span> {{ $t('press.mediaKit.shareLink') }}
            </button>
            <a href="#" target="_blank" class="btn btn-outline">
              <span>👁</span> {{ $t('press.mediaKit.viewFullSize') }}
            </a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const shareMediaKit = () => {
  const url = window.location.origin + '/media-kit'

  // Check if Web Share API is available
  if (navigator.share) {
    navigator
      .share({
        title: 'The Socioscope Media Kit',
        text: 'Check out The Socioscope Media Kit - investigating what truly drives sustainable change',
        url: url
      })
      .catch((error) => console.log('Error sharing:', error))
  } else {
    // Fallback: copy to clipboard
    navigator.clipboard
      .writeText(url)
      .then(() => {
        alert('Link copied to clipboard! Share it with others.')
      })
      .catch(() => {
        alert('Link: ' + url)
      })
  }
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section {
  padding: 5rem 0;
}

.section-white {
  background: $cream;
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

.media-kit-section {
  max-width: 900px;
  margin: 0 auto;
}

.media-kit-card {
  background: white;
  border: 2px solid $warm-beige;
  padding: 3rem;
  margin-bottom: 3rem;
  transition: all 0.3s ease;

  &:hover {
    border-color: $green-bright;
    box-shadow: 0 12px 36px rgba(44, 36, 22, 0.15);
  }
}

.media-kit-header {
  display: flex;
  align-items: center;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid $warm-beige;
}

.media-kit-icon {
  font-size: 4rem;
  flex-shrink: 0;
}

.media-kit-info {
  h3 {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    margin-bottom: 0.5rem;
    color: $forest-green;
    font-weight: 700;
  }

  p {
    font-size: 1.1rem;
    opacity: 0.8;
  }
}

.media-kit-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-item {
  text-align: center;
  padding: 1.5rem;
  background: $warm-beige;
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: $green-bright;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.9rem;
  opacity: 0.8;
}

.media-kit-preview {
  margin-bottom: 2rem;

  img {
    width: 100%;
    height: auto;
    border: 1px solid $warm-beige;
  }
}

.media-kit-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
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

.btn-outline {
  background: transparent;
  color: $brown-dark;
  border-color: $brown-dark;

  &:hover {
    background: $brown-dark;
    color: $cream;
  }
}

@media (max-width: 1024px) {
  .media-kit-stats {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .section {
    padding: 4rem 0;
  }

  .media-kit-card {
    padding: 2rem 1.5rem;
  }

  .media-kit-header {
    flex-direction: column;
    text-align: center;
  }

  .media-kit-stats {
    grid-template-columns: 1fr;
  }

  .media-kit-actions {
    flex-direction: column;
  }

  .btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
