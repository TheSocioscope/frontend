<template>
  <v-card class="project-timeline mb-4" elevation="2" id="milestones">
    <v-card-title class="section-title">
      <v-icon class="mr-2" color="#4ca049">mdi-flag-checkered</v-icon>
      {{ $t('projects.detail.timeline') }}
    </v-card-title>

    <v-card-text class="px-4 pb-6">
      <v-timeline
        side="end"
        align="start"
        line-color="#4ca049"
        line-thickness="2"
        truncate-line="both"
      >
        <v-timeline-item
          v-for="(item, index) in localizedTimeline"
          :key="index"
          :dot-color="index === 0 ? '#27421d' : '#4ca049'"
          :icon="item.icon || 'mdi-circle-small'"
          fill-dot
          size="small"
          class="milestone-item"
          :style="{ animationDelay: `${index * 0.08}s` }"
        >
          <v-card class="milestone-card" :elevation="index === 0 ? 3 : 1" rounded="lg">
            <v-card-text class="pa-3">
              <div class="milestone-date">{{ item.date }}</div>
              <p class="milestone-description ma-0">{{ item.text }}</p>
            </v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  localizedTimeline: Array<{ date: string; text: string; icon?: string }>
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #27421d;
}

.milestone-item {
  opacity: 0;
  animation: fadeInLeft 0.5s ease-out forwards;
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-12px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.milestone-card {
  border-left: 3px solid #4ca049;
  background-color: #fffbf0;
  transition:
    box-shadow 0.2s ease,
    transform 0.2s ease;

  &:hover {
    box-shadow: 0 4px 16px rgba(76, 160, 73, 0.2) !important;
    transform: translateX(2px);
  }
}

.milestone-date {
  font-weight: 800;
  color: #27421d;
  font-size: 0.95rem;
  letter-spacing: 0.02em;
  text-transform: uppercase;
  margin-bottom: 4px;
}

.milestone-description {
  color: #2c2416;
  line-height: 1.6;
  font-size: 1.05rem;
}
</style>
