<template>
  <header id="about" class="project-header">
    <!-- Tags row -->
    <div class="tags-row">
      <span v-if="primarySector" class="tag">
        <v-icon size="x-small">mdi-leaf</v-icon>
        {{ primarySector }}
      </span>
      <span v-if="locationLabel" class="tag">{{ locationLabel }}</span>
      <span v-if="sizeLabel" class="tag">{{ sizeLabel }}</span>
    </div>

    <!-- Hero grid: text left, actions right -->
    <div class="hero-grid">
      <div class="hero-text">
        <h1 class="hero-title">{{ localizedName }}</h1>
        <p v-if="project.entityDescription" class="hero-entity">
          {{ project.entityDescription }}
        </p>
        <p v-if="localizedDescription" class="hero-description">
          {{ localizedDescription }}
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
        <!-- Social icons row -->
        <div v-if="socialLinks.length" class="social-row">
          <a
            v-for="link in socialLinks"
            :key="link.platform"
            :href="link.url"
            target="_blank"
            rel="noopener noreferrer"
            class="social-icon"
            :aria-label="link.platform"
          >
            <v-icon size="18">{{ link.icon }}</v-icon>
          </a>
        </div>
        <!-- Suggest edit -->
        <button class="btn-edit" @click="$emit('edit')">
          <v-icon size="small">mdi-pencil-outline</v-icon>
          {{ $t('projects.detail.suggestEdit', 'Suggest an edit') }}
        </button>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
const props = defineProps<{
  project: any
  localizedName: string
  localizedDescription?: string
}>()

defineEmits<{ connect: []; edit: [] }>()

const { t: $t } = useI18n()

const locationLabel = computed(() => {
  if (props.project?.location) return props.project.location
  const countries = props.project?.country
  if (Array.isArray(countries) && countries.length) return countries[0]
  return null
})

const primarySector = computed(() => {
  const sectors = props.project?.sectorFocus
  return Array.isArray(sectors) && sectors.length ? sectors[0] : null
})

const sizeLabel = computed(() => {
  const parts = [props.project?.entitySize, props.project?.entityRole?.[0]].filter(Boolean)
  return parts.length ? parts.join(' · ') : null
})

const detectPlatform = (url: string): { platform: string; icon: string } | null => {
  if (!url) return null
  if (url.includes('facebook.com') || url.includes('fb.com'))
    return { platform: 'Facebook', icon: 'mdi-facebook' }
  if (url.includes('instagram.com'))
    return { platform: 'Instagram', icon: 'mdi-instagram' }
  if (url.includes('twitter.com') || url.includes('x.com'))
    return { platform: 'Twitter / X', icon: 'mdi-twitter' }
  if (url.includes('linkedin.com'))
    return { platform: 'LinkedIn', icon: 'mdi-linkedin' }
  if (url.includes('youtube.com') || url.includes('youtu.be'))
    return { platform: 'YouTube', icon: 'mdi-youtube' }
  return null
}

const socialLinks = computed(() => {
  const links: { platform: string; icon: string; url: string }[] = []
  // Detect social platform from the url field
  if (props.project?.url) {
    const detected = detectPlatform(props.project.url)
    if (detected) links.push({ ...detected, url: props.project.url })
  }
  // YouTube from the yt field
  if (props.project?.yt) {
    links.push({ platform: 'YouTube', icon: 'mdi-youtube', url: `https://www.youtube.com/watch?v=${props.project.yt}` })
  }
  return links
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
  justify-content: center;
  gap: 4px;
  font-size: 11px;
  font-family: $font-family-base;
  border-radius: 999px;
  padding: 3px 10px;
  white-space: nowrap;
  font-weight: 700;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  color: $green-forest;
  background: rgba(76, 160, 73, 0.1);
  border: 0.5px solid rgba(76, 160, 73, 0.3);
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
  font-size: 1.625rem; /* 26px */
  font-weight: $font-weight-semibold; /* 600 — loaded weight */
  line-height: 1.2;
  color: $earth-95;
  text-transform: uppercase;
  letter-spacing: 0.01em;
  margin: 0 0 $rhythm-1;

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 1.25rem;
  }
}

.hero-entity {
  font-size: 12px;
  font-weight: 600;
  color: $green-forest;
  margin: 0 0 6px;
  line-height: 1.4;
}

.hero-description {
  font-size: 13px;
  color: $text-secondary;
  margin: 0;
  line-height: 1.6;
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
    border-color: $green-leaf;
    color: $green-leaf;
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

.btn-edit {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  background: none;
  border: 0.5px solid $border-soft;
  border-radius: 10px;
  padding: 7px 14px;
  font-family: $font-family-base;
  font-size: 11px;
  font-weight: 600;
  color: $text-caption;
  cursor: pointer;
  width: 100%;
  letter-spacing: 0.03em;
  transition:
    border-color $transition-fast,
    color $transition-fast;

  &:hover {
    border-color: $green-leaf;
    color: $green-forest;
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

/* Social icons row */
.social-row {
  display: flex;
  gap: 6px;
  width: 100%;
}

.social-icon {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 34px;
  background: $earth-5;
  border: 0.5px solid $border-soft;
  border-radius: 8px;
  color: $text-secondary;
  text-decoration: none;
  transition:
    border-color $transition-fast,
    color $transition-fast,
    background $transition-fast;

  &:hover {
    border-color: rgba(76, 160, 73, 0.5);
    color: $green-leaf;
    background: rgba(76, 160, 73, 0.06);
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}
</style>
