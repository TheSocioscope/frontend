<template>
  <v-card
    v-if="localizedTimeline && localizedTimeline.length > 0"
    id="timeline"
    class="project-timeline"
  >
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-timeline-clock-outline</v-icon>
      {{ $t('common.milestones') }}
    </v-card-title>
    <v-card-text>
      <v-timeline side="end" align="start" truncate-line="both" density="comfortable">
        <v-timeline-item
          v-for="(item, index) in localizedTimeline"
          :key="index"
          :dot-color="getTimelineColor(index)"
          size="small"
        >
          <template #opposite>
            <div class="timeline-date">{{ item.date }}</div>
          </template>

          <v-card class="timeline-card" elevation="2">
            <v-card-text>
              <div class="timeline-content">{{ item.text }}</div>
            </v-card-text>
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  localizedTimeline: Array<{ date: string; text: string }>
}>()

const { t: $t } = useI18n()

const colors = ['primary', 'secondary', 'accent', 'success', 'info', 'warning']

const getTimelineColor = (index: number) => {
  return colors[index % colors.length]
}
</script>

<style scoped lang="scss">
.project-timeline {
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

.timeline-date {
  font-size: 0.95rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.6);
  padding-right: 1rem;
  text-align: right;
}

.timeline-card {
  margin-bottom: 0.5rem;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15) !important;
  }
}

.timeline-content {
  font-size: 1rem;
  line-height: 1.6;
  color: rgba(0, 0, 0, 0.87);
}

@media (max-width: 768px) {
  .timeline-date {
    text-align: left;
    padding-right: 0;
    padding-bottom: 0.5rem;
  }
}
</style>
