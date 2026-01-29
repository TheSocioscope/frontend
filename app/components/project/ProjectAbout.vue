<template>
  <v-card id="about" class="project-about">
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-information-outline</v-icon>
      {{ $t('projects.detail.about') }}
    </v-card-title>
    <v-card-text>
      <div class="description-content" v-html="localizedDescription" />

      <v-divider v-if="project.contact" class="my-4" />

      <div v-if="project.contact" class="contact-info">
        <h3 class="contact-title">{{ $t('nav.contact') }}</h3>
        <div class="contact-details">
          <div v-if="project.contact.entity">
            <strong>{{ $t('common.organization') }}:</strong> {{ project.contact.entity }}
          </div>
          <div v-if="project.contact.firstname || project.contact.lastname">
            <strong>{{ $t('common.contact') }}:</strong>
            {{ project.contact.firstname }} {{ project.contact.lastname }}
          </div>
          <div v-if="project.contact.contact_url">
            <v-btn
              :href="project.contact.contact_url"
              target="_blank"
              variant="outlined"
              size="small"
              prepend-icon="mdi-email"
            >
              {{ $t('nav.contactUs') }}
            </v-btn>
          </div>
        </div>
      </div>
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

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
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
