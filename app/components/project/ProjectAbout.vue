<template>
  <section id="about" class="project-about">
    <ProjectSectionHeader icon="mdi-information-outline">
      {{ $t('projects.detail.about') }}
    </ProjectSectionHeader>
    <p v-if="project.entityDescription" class="entity-summary">
      {{ project.entityDescription }}
    </p>
    <div class="description-content" v-html="localizedDescription" />
  </section>
</template>

<script setup lang="ts">
defineProps<{
  project: any
  localizedDescription: string
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-about {
  margin-bottom: $rhythm-6;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $sticky-section-nav + $rhythm-2;

  @media (max-width: $detail-bp-tablet - 1) {
    margin-bottom: $rhythm-3;
  }
}

.entity-summary {
  font-size: 1.15rem;
  font-weight: 600;
  color: $green-dark;
  line-height: 1.6;
  margin: 0 0 $rhythm-2;
  padding-bottom: $rhythm-2;
  border-bottom: 2px solid rgba(76, 160, 73, 0.2);

  /* Tighter sizing on mobile — this is now the only place the entity
     description shows on phone (page header drops it). */
  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 1rem;
    line-height: 1.45;
    padding-bottom: $rhythm-1;
    margin-bottom: $rhythm-2;
  }
}

.description-content {
  font-size: 1.0625rem;
  line-height: 1.7;
  color: $text-primary;

  :deep(p) {
    margin-bottom: $rhythm-2;
  }

  :deep(ul),
  :deep(ol) {
    margin-left: $rhythm-3;
    margin-bottom: $rhythm-2;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 0.9375rem;
    line-height: 1.6;

    :deep(p) {
      margin-bottom: 8px;
    }
  }
}
</style>
