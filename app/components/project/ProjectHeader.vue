<template>
  <header id="about" class="project-header">
    <div class="floating-element floating-element-1" aria-hidden="true" />
    <div class="floating-element floating-element-2" aria-hidden="true" />
    <div class="floating-element floating-element-3" aria-hidden="true" />
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
  position: relative;
  overflow: hidden;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $sticky-section-nav + $rhythm-2;

  :deep(.v-container) {
    /* The header lives inside the main column of detail-grid; let the
       column define the width and the v-container be a simple flow box. */
    max-width: 100%;
    padding: 0;
    position: relative;
    z-index: 1;
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

.floating-element {
  position: absolute;
  border-radius: 50%;
  opacity: 0.12;
  animation: float 6s ease-in-out infinite;
  pointer-events: none;
}

.floating-element-1 {
  width: 120px;
  height: 120px;
  background: $green-bright;
  top: 10%;
  right: 8%;
  animation-delay: 0s;
}

.floating-element-2 {
  width: 80px;
  height: 80px;
  background: $brown-dark;
  bottom: 15%;
  right: 20%;
  animation-delay: 1s;
}

.floating-element-3 {
  width: 100px;
  height: 100px;
  background: $green-bright;
  top: 30%;
  right: 35%;
  animation-delay: 2s;
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0) translateX(0);
  }
  25% {
    transform: translateY(-20px) translateX(10px);
  }
  50% {
    transform: translateY(-10px) translateX(-10px);
  }
  75% {
    transform: translateY(-25px) translateX(5px);
  }
}
</style>
