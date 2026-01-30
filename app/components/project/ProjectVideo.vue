<template>
  <v-card v-if="project.yt" class="project-video">
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-video-outline</v-icon>
      {{ $t('projects.detail.video') }}
    </v-card-title>
    <v-card-text>
      <div class="video-container">
        <iframe
          :src="`https://www.youtube.com/embed/${project.yt}`"
          frameborder="0"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
          allowfullscreen
          class="video-iframe"
        />
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  project: any
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
.project-video {
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

.video-container {
  position: relative;
  padding-bottom: 56.25%; /* 16:9 aspect ratio */
  height: 0;
  overflow: hidden;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 8px;
}
</style>
