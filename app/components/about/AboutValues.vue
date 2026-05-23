<template>
  <section class="section values-section">
    <v-container>
      <div class="values-wrapper section-reveal">
        <h2 class="values-title">{{ $t('about.values.title') }}</h2>
        <div class="values-grid">
          <div v-for="(value, index) in values" :key="index" class="value-card">
            <div class="value-card__head">
              <span class="value-icon" aria-hidden="true">{{ value.icon }}</span>
              <h3>{{ $t(value.titleKey) }}</h3>
            </div>
            <p>{{ $t(value.descKey) }}</p>
          </div>
        </div>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const values = [
  {
    icon: '🌍',
    titleKey: 'about.values.global.title',
    descKey: 'about.values.global.desc'
  },
  {
    icon: '🤝',
    titleKey: 'about.values.collaboration.title',
    descKey: 'about.values.collaboration.desc'
  },
  {
    icon: '🔓',
    titleKey: 'about.values.open.title',
    descKey: 'about.values.open.desc'
  },
  {
    icon: '⚖️',
    titleKey: 'about.values.ethical.title',
    descKey: 'about.values.ethical.desc'
  }
]
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.values-section {
  background: $warm-beige;
  padding: 2.5rem 0;

  @media (max-width: 768px) {
    padding: 2rem 0;
  }
}

.values-wrapper {
  display: grid;
  grid-template-columns: minmax(0, 220px) minmax(0, 1fr);
  gap: 2.5rem;
  align-items: start;

  @media (max-width: 960px) {
    grid-template-columns: 1fr;
    gap: 1.25rem;
  }
}

.values-title {
  font-size: 2rem;
  margin: 0;
  color: $brown-dark;
  font-family: $font-family-display;
  font-weight: $font-weight-bold;
  line-height: 1.15;
  position: sticky;
  top: 1rem;

  @media (max-width: 960px) {
    font-size: 1.625rem;
    position: static;
    text-align: center;
  }
}

.values-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;

  @media (max-width: 960px) {
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
  }

  // Phones: keep a 2×2 so all four values fit on screen at a glance
  // (no scrolling). Tight gaps; the card styles below keep each tile short.
  @media (max-width: 600px) {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.625rem;
  }
}

.value-card {
  display: flex;
  flex-direction: column;
  gap: 0.625rem;
  text-align: left;
  background: $cream;
  padding: 1.125rem 1.125rem 1.125rem 1.25rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-left: 3px solid $green-bright;
  border-radius: 6px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 14px rgba(44, 36, 22, 0.08);
  }

  // Icon sits beside the title so narrow phone cards don't waste a whole row.
  &__head {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  // Bare emoji inline with the title — matches the clean header treatment
  // rather than sitting in a separate chip.
  .value-icon {
    flex-shrink: 0;
    font-size: 1.5rem;
    line-height: 1;
  }

  h3 {
    font-size: 1rem;
    margin: 0;
    color: $forest-green;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    line-height: 1.25;
  }

  p {
    font-size: 0.875rem;
    line-height: 1.55;
    color: $brown-dark;
    opacity: 0.78;
    margin: 0;
    font-family: $font-family-display;
  }

  // Phones: compact, centred tiles so the 2×2 grid fits on one screen.
  // The icon badge stacks above the title (centred) so a wrapping title
  // stays balanced instead of pushing the icon off to one side.
  @media (max-width: 600px) {
    gap: 0.5rem;
    padding: 1rem 0.75rem;
    border-left-width: 3px;
    border-radius: 8px;
    text-align: center;

    &__head {
      flex-direction: column;
      align-items: center;
      gap: 0.4375rem;
    }

    .value-icon {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 36px;
      height: 36px;
      font-size: 1.25rem;
      border-radius: 50%;
      background: rgba(76, 160, 73, 0.12);
    }

    h3 {
      font-size: 0.875rem;
      line-height: 1.25;
    }

    p {
      font-size: 0.75rem;
      line-height: 1.45;
    }
  }
}
</style>
