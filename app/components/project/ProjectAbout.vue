<template>
  <v-card id="about" class="project-about">
    <ProjectSectionHeader icon="mdi-information-outline">
      {{ $t('projects.detail.about') }}
    </ProjectSectionHeader>
    <v-card-text>
      <div class="description-content" v-html="localizedDescription" />

    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  project: any
  localizedDescription: string
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
.project-about {
  margin-bottom: 2rem;
}

.description-content {
  font-size: 1.1rem;
  line-height: 1.8;
  color: rgba(0, 0, 0, 0.87);

  :deep(p) {
    margin-bottom: 1rem;
  }

  :deep(ul),
  :deep(ol) {
    margin-left: 1.5rem;
    margin-bottom: 1rem;
  }
}

.contact-info {
  margin-top: 1rem;
}

.contact-title {
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: rgba(0, 0, 0, 0.87);
}

.contact-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;

  div {
    font-size: 1rem;
  }

  strong {
    color: rgba(0, 0, 0, 0.87);
    margin-right: 0.5rem;
  }
}
</style>
