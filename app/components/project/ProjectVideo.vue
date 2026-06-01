<template>
  <section v-if="project.yt" id="video" class="project-video">
    <span class="section-label">{{ $t('projects.detail.video') }}</span>
    <div class="video-container">
      <iframe
        :src="`https://www.youtube.com/embed/${project.yt}`"
        frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowfullscreen
        class="video-iframe"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  project: any
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-video {
  margin-bottom: $rhythm-6;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $rhythm-2;
}

.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $text-secondary;
  margin-bottom: $rhythm-2;
}

.video-container {
  position: relative;
  padding-bottom: 56.25%;
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
