<template>
  <header id="about" class="project-header">
    <v-container>
      <h1 class="initiative-name">{{ localizedName }}</h1>

      <div v-if="project.location" class="location">
        <v-icon size="small">mdi-map-marker</v-icon>
        <span>{{ project.location }}</span>
      </div>

      <p v-if="project.entityDescription" class="entity-summary">
        {{ project.entityDescription }}
      </p>

      <div
        v-if="localizedDescription"
        class="description-content"
        v-html="localizedDescription"
      />
    </v-container>
  </header>
</template>

<script setup lang="ts">
defineProps<{
  project: any
  localizedName: string
  localizedDescription?: string
  showOriginal: boolean
  showDisclaimer: boolean
}>()

defineEmits<{
  'toggle-language': []
}>()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-header {
  background-color: $warm-beige;
  padding: $rhythm-4;
  border-radius: 8px;
  margin-bottom: $rhythm-3;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $sticky-section-nav + $rhythm-2;

  :deep(.v-container) {
    /* The header lives inside the main column of detail-grid; let the
       column define the width and the v-container be a simple flow box. */
    max-width: 100%;
    padding: 0;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    padding: $rhythm-2 $rhythm-2 $rhythm-3;
    border-radius: 0;
    margin-left: -$gutter-mobile;
    margin-right: -$gutter-mobile;
    margin-bottom: $rhythm-2;
  }
}

.initiative-name {
  font-size: 2.25rem;
  line-height: 1.15;
  font-weight: 700;
  color: $green-dark;
  margin: 0 0 $rhythm-1;
}

.location {
  display: flex;
  align-items: center;
  gap: $rhythm-1;
  font-size: 1rem;
  color: $brown-dark;
  margin-bottom: $rhythm-3;
}

.entity-summary {
  font-size: 1.15rem;
  font-weight: 600;
  color: $green-dark;
  line-height: 1.55;
  margin: 0 0 $rhythm-2;
  padding-bottom: $rhythm-2;
  border-bottom: 2px solid rgba(76, 160, 73, 0.2);
}

.description-content {
  font-size: 1.0625rem;
  line-height: 1.7;
  color: $text-primary;

  :deep(p) {
    margin-bottom: $rhythm-2;
  }

  :deep(p:last-child) {
    margin-bottom: 0;
  }

  :deep(ul),
  :deep(ol) {
    margin-left: $rhythm-3;
    margin-bottom: $rhythm-2;
  }
}

@media (max-width: $detail-bp-tablet - 1) {
  .initiative-name {
    font-size: 1.4rem;
    line-height: 1.2;
  }

  .location {
    font-size: 0.875rem;
    margin-bottom: $rhythm-2;
  }

  .entity-summary {
    font-size: 1rem;
    line-height: 1.45;
    padding-bottom: $rhythm-1;
    margin-bottom: $rhythm-2;
  }

  .description-content {
    font-size: 0.9375rem;
    line-height: 1.6;

    :deep(p) {
      margin-bottom: 8px;
    }
  }
}
</style>
