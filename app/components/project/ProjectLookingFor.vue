<template>
  <section id="looking-for" class="project-looking-for">
    <ProjectSectionHeader icon="mdi-magnify">
      {{ $t('projects.detail.lookingFor') }}
    </ProjectSectionHeader>
    <div class="offering-cloud">
      <div
        v-for="(item, index) in localizedLookingFor"
        :key="index"
        class="offering-chip"
        :class="`tone-${index % 2}`"
      >
        <span class="offering-emoji" aria-hidden="true">{{ getEmoji(item.icon) }}</span>
        <span class="offering-text">{{ item.title }}</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
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
@use '~~/assets/styles/variables' as *;

.project-looking-for {
  margin-bottom: $rhythm-6;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $sticky-section-nav + $rhythm-2;

  @media (max-width: $detail-bp-tablet - 1) {
    margin-bottom: $rhythm-3;
  }
}

/* Lay the items out as an even grid so they fill the section width instead of
   trailing off down the left edge: two equal columns on tablet/desktop, a
   single stacked column on phones. Each chip stretches to fill its cell, so
   short and long items line up tidily. */
.offering-cloud {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  align-items: stretch;
  gap: 12px;

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}

.offering-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 16px;
  border-radius: 12px;
  font-family: $font-family-base;
  font-size: 0.9375rem;
  font-weight: 500;
  line-height: 1.35;
  color: $text-primary;
  border: 1px solid transparent;
  cursor: default;
  min-width: 0;
  box-sizing: border-box;
  transition:
    box-shadow 0.2s,
    border-color 0.2s;

  &:hover {
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
    border-color: rgba(76, 160, 73, 0.25);
  }

  /* Two warm tones alternating — subtle rhythm without visual noise. */
  &.tone-0 {
    background: $earth-10;
  }
  &.tone-1 {
    background: $saffron-pale;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    padding: 10px 14px;
    font-size: 0.8125rem;
    gap: 8px;
  }
}

.offering-emoji {
  font-size: 1.05em;
  line-height: 1;
  flex-shrink: 0;
}

.offering-text {
  /* Long phrases wrap inside the cell rather than overflowing it. */
  min-width: 0;
  word-break: break-word;
  overflow-wrap: anywhere;
}
</style>
