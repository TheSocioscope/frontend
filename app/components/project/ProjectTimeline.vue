<template>
  <v-card class="project-timeline mb-4" elevation="2" id="milestones">
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-flag-checkered</v-icon>
      {{ $t('common.milestones') }}
    </v-card-title>

    <v-card-text>
      <div class="timeline">
        <div
          v-for="(item, index) in localizedTimeline"
          :key="index"
          class="milestone"
          :style="{ animationDelay: `${index * 0.1}s` }"
        >
          <div class="milestone-date">{{ item.date }}</div>
          <div class="milestone-description">{{ item.text }}</div>
        </div>
      </div>
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

.timeline {
  position: relative;
  padding-left: 40px;

  &::before {
    content: '';
    position: absolute;
    left: 15px;
    top: 0;
    bottom: 0;
    width: 3px;
    background-color: #4ca049;
  }
}

.milestone {
  position: relative;
  margin-bottom: 30px;
  opacity: 0;
  animation: fadeInUp 0.6s forwards;

  &::before {
    content: '';
    position: absolute;
    left: -33px;
    top: 5px;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background-color: #4ca049;
    border: 3px solid #fffbf0;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.milestone-date {
  font-weight: 800;
  color: #27421d;
  font-size: 1.1em;
}

.milestone-description {
  color: #2c2416;
  margin-top: 5px;
  line-height: 1.6;
  font-size: 1.15em;
}
</style>
