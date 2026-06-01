<template>
  <header id="about" class="project-header">
    <!-- Tags row -->
    <div class="tags-row">
      <span v-if="primarySector" class="tag tag--green">
        <v-icon size="x-small">mdi-leaf</v-icon>
        {{ primarySector }}
      </span>
      <span v-if="project.location" class="tag">
        <v-icon size="x-small">mdi-map-pin</v-icon>
        {{ project.location }}
      </span>
      <span v-if="sizeLabel" class="tag tag--muted">{{ sizeLabel }}</span>
    </div>

    <!-- Hero grid: text left, actions right -->
    <div class="hero-grid">
      <div class="hero-text">
        <h1 class="hero-title">{{ localizedName }}</h1>
        <p v-if="project.entityDescription" class="hero-entity">
          {{ project.entityDescription }}
        </p>
      </div>

      <div class="hero-actions">
        <button class="btn-contact" @click="$emit('connect')">
          <v-icon size="small">mdi-email-outline</v-icon>
          {{ $t('projects.detail.connect', 'Contact') }}
        </button>
        <a
          v-if="project.url"
          :href="project.url"
          target="_blank"
          rel="noopener noreferrer"
          class="btn-website"
        >
          <v-icon size="small">mdi-web</v-icon>
          {{ $t('projects.detail.website', 'Website') }}
        </a>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
const props = defineProps<{
  project: any
  localizedName: string
}>()

defineEmits<{ connect: [] }>()

const { t: $t } = useI18n()

const primarySector = computed(() => {
  const sectors = props.project?.sectorFocus
  return Array.isArray(sectors) && sectors.length ? sectors[0] : null
})

const sizeLabel = computed(() => {
  const parts = [props.project?.entitySize, props.project?.entityRole?.[0]].filter(Boolean)
  return parts.length ? parts.join(' · ') : null
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-header {
  padding: $rhythm-4 0 $rhythm-3;
  border-bottom: 0.5px solid $border-soft;
  margin-bottom: $rhythm-4;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $rhythm-2;
}

/* Tags row */
.tags-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px;
  margin-bottom: $rhythm-3;
}

.tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  font-family: $font-family-base;
  border: 0.5px solid $border-soft;
  border-radius: 999px;
  padding: 3px 10px;
  color: $text-secondary;
  background: $earth-5;
  white-space: nowrap;
}

.tag--green {
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: $green-forest;
  background: rgba(76, 160, 73, 0.1);
  border-color: rgba(76, 160, 73, 0.3);
}

.tag--muted {
  color: $text-caption;
}

/* Hero grid: text left, actions right */
.hero-grid {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: $rhythm-6;
  align-items: flex-start;

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: 1fr;
    gap: $rhythm-3;
  }
}

.hero-text {
  min-width: 0;
}

.hero-title {
  font-family: $font-family-display;
  font-size: clamp(1.75rem, 4vw, 2.5rem);
  font-weight: $font-weight-medium;
  line-height: 1.1;
  color: $earth-95;
  margin: 0 0 $rhythm-1;
}

.hero-entity {
  font-size: 13px;
  font-weight: 700;
  color: $green-forest;
  margin: 0;
  line-height: 1.4;
}

/* Action column */
.hero-actions {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: $rhythm-1;
  min-width: 160px;

  @media (max-width: $detail-bp-tablet - 1) {
    flex-direction: row;
    flex-wrap: wrap;
    min-width: 0;
  }
}

.btn-contact {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 7px;
  background: $green-forest;
  color: white;
  border: none;
  border-radius: 10px;
  padding: 11px 18px;
  font-family: $font-family-base;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  width: 100%;
  transition: background $transition-fast;

  &:hover {
    background: $green-leaf-dark;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    flex: 1;
    width: auto;
  }
}

.btn-website {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: none;
  border: 0.5px solid $border-soft;
  border-radius: 10px;
  padding: 8px 14px;
  font-family: $font-family-base;
  font-size: 12px;
  color: $text-secondary;
  text-decoration: none;
  transition:
    border-color $transition-fast,
    color $transition-fast;

  &:hover {
    border-color: $border-strong;
    color: $text-primary;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    flex: 1;
    width: auto;
  }
}
</style>
