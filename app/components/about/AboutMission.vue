<template>
  <section class="section mission-section">
    <v-container>
      <div class="mission-grid section-reveal">
        <div class="mission-text">
          <h2>{{ $t('about.mission.title') }}</h2>
          <p>{{ $t('about.mission.paragraph1') }}</p>
          <p>{{ $t('about.mission.paragraph2') }}</p>
        </div>
        <ul class="info-circles">
          <li v-for="(item, index) in infoItems" :key="index" class="info-circle">
            <span class="info-icon" aria-hidden="true">{{ item.icon }}</span>
            <h3>{{ $t(item.labelKey) }}</h3>
            <p class="info-value">{{ $t(item.valueKey) }}</p>
            <p class="info-detail">{{ $t(item.detailKey) }}</p>
          </li>
        </ul>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const infoItems = [
  {
    icon: '🌱',
    labelKey: 'about.info.established.label',
    valueKey: 'about.info.established.value',
    detailKey: 'about.info.established.detail'
  },
  {
    icon: '🥐',
    labelKey: 'about.info.location.label',
    valueKey: 'about.info.location.value',
    detailKey: 'about.info.location.detail'
  },
  {
    icon: '🌍',
    labelKey: 'about.info.reach.label',
    valueKey: 'about.info.reach.value',
    detailKey: 'about.info.reach.detail'
  }
]
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.mission-section {
  background: $cream;
  padding: 3rem 0;

  @media (max-width: 768px) {
    padding: 2.5rem 0;
  }
}

/* 2-col on desktop: text on the left, info cards on the right (vertically
   centred against the text). The layout itself stays left-aligned — only
   the paragraph text is justified to align with the info column edge. */
.mission-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, 1fr);
  gap: 3rem;
  align-items: center;

  @media (max-width: 960px) {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    align-items: stretch;
  }
}

.mission-text {
  h2 {
    font-size: 2rem;
    margin: 0 0 1rem;
    color: $brown-dark;
    font-family: $font-family-display;
    font-weight: $font-weight-bold;
    line-height: 1.15;

    @media (max-width: 768px) {
      font-size: 1.625rem;
      /* Mobile: centre the title so it aligns with the centred paragraphs */
      text-align: center;
    }
  }

  p {
    margin: 0 0 0.875rem;
    font-size: 1rem;
    line-height: 1.65;
    color: $brown-dark;
    font-family: $font-family-display;
    /* Desktop: justified text gives the column a clean editorial edge.
       Mobile: centre-aligned reads better on narrow widths. */
    text-align: justify;
    hyphens: auto;

    @media (max-width: 768px) {
      text-align: center;
      hyphens: manual;
    }

    &:last-child {
      margin-bottom: 0;
    }
  }
}

/* 2-on-top, 1-below equilateral cluster. The third item spans both
   tracks and centres itself; the row-gap is computed so the bottom
   circle sits at the third vertex of an equilateral triangle —
   making the visible edge-to-edge distance identical for every pair. */
.info-circles {
  --circle-size: clamp(150px, 16vw, 188px);
  --pair-gap: 1.5rem;

  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, auto);
  column-gap: var(--pair-gap);
  row-gap: calc((var(--circle-size) + var(--pair-gap)) * 0.866 - var(--circle-size));
  justify-content: center;

  > :nth-child(3) {
    grid-column: 1 / -1;
    justify-self: center;
  }
}

.info-circle {
  position: relative;
  width: var(--circle-size);
  height: var(--circle-size);
  border-radius: 50%;
  background: $surface-card;
  border: 1px solid $border-soft;
  box-shadow: 0 2px 10px rgba(44, 36, 22, 0.05);

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 0.875rem 1rem;

  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;

  /* Subtle inner ring on hover for depth without a hard outline. */
  &::after {
    content: '';
    position: absolute;
    inset: 6px;
    border-radius: 50%;
    border: 1px dashed transparent;
    transition: border-color 0.25s ease;
    pointer-events: none;
  }

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 28px rgba(44, 36, 22, 0.1);
    border-color: $green-leaf;

    &::after {
      border-color: rgba(76, 160, 73, 0.35);
    }
  }
}

.info-icon {
  font-size: 1.6rem;
  line-height: 1;
  margin-bottom: 0.4rem;
}

.info-circle h3 {
  font-size: 0.6rem;
  text-transform: uppercase;
  letter-spacing: 0.14em;
  color: $forest-green;
  margin: 0 0 0.15rem;
  font-weight: $font-weight-semibold;
  font-family: $font-family-display;
}

.info-value {
  font-size: 0.95rem;
  font-weight: $font-weight-bold;
  color: $brown-dark;
  line-height: 1.2;
  margin: 0 0 0.2rem;
  font-family: $font-family-display;
}

.info-detail {
  font-size: 0.7rem;
  font-weight: $font-weight-regular;
  color: $brown-dark;
  opacity: 0.65;
  margin: 0;
  line-height: 1.3;
  font-family: $font-family-display;
  max-width: 80%;
}
</style>
