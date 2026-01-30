<template>
  <v-card class="project-looking-for mb-4" elevation="2" id="lookingFor">
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-magnify</v-icon>
      {{ $t('projects.detail.lookingFor') }}
    </v-card-title>

    <v-card-text>
      <div class="offering-items">
        <div v-for="(item, index) in localizedLookingFor" :key="index" class="offering-item">
          <span class="offering-emoji">{{ getEmoji(item.icon) }}</span>
          <span class="offering-text">{{ item.title }}</span>
        </div>
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
const props = defineProps<{
  localizedLookingFor: Array<{ title: string; description?: string; icon?: string }>
}>()

const { t: $t } = useI18n()

const getEmoji = (icon?: string) => {
  if (!icon) return '🔍'
  const emojiMap: Record<string, string> = {
    funding: '💰',
    awareness: '📢',
    partnership: '🤝',
    collaboration: '👥',
    certification: '📜',
    'tech-funding': '💻',
    cooperative: '🌾'
  }
  return emojiMap[icon] || '🔍'
}
</script>

<style scoped lang="scss">
.section-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: #27421d;
}

.offering-items {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.offering-item {
  background-color: #f5edd6;
  padding: 12px 20px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 10px;
  border: 2px solid #4ca049;
  font-size: 1em;
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-2px);
  }
}

.offering-emoji {
  font-size: 1.2em;
}

.offering-text {
  color: #2c2416;
  font-weight: 500;
}
</style>
