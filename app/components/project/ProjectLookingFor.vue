<template>
  <!-- Column mode: used inside the exchange board -->
  <div v-if="column" class="needs-column">
    <div class="col-header">
      <div class="col-header-icon col-header-icon--warm" aria-hidden="true">
        <v-icon size="x-small" color="#854F0B">mdi-magnify</v-icon>
      </div>
      <span class="col-header-label col-header-label--warm">
        {{ $t('projects.detail.lookingFor') }}
      </span>
    </div>
    <div class="needs-list">
      <div v-for="(item, index) in localizedLookingFor" :key="index" class="need-card">
        <div class="need-icon" aria-hidden="true">
          <v-icon size="small" color="#854F0B">{{ getMdiIcon(item.icon) }}</v-icon>
        </div>
        <div class="need-body">
          <p class="need-title">{{ item.title }}</p>
          <p v-if="item.description" class="need-desc">{{ item.description }}</p>
        </div>
      </div>
    </div>
  </div>

  <!-- Standalone section mode (default) -->
  <section v-else id="looking-for" class="project-looking-for">
    <span class="section-label">{{ $t('projects.detail.lookingFor') }}</span>
    <div class="chips-grid">
      <div
        v-for="(item, index) in localizedLookingFor"
        :key="index"
        class="chip"
        :class="`tone-${index % 2}`"
      >
        <span class="chip-emoji" aria-hidden="true">{{ getEmoji(item.icon) }}</span>
        <span class="chip-text">{{ item.title }}</span>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  localizedLookingFor: Array<{ title: string; description?: string; icon?: string }>
  column?: boolean
}>()

const { t: $t } = useI18n()

const getMdiIcon = (icon?: string): string => {
  if (!icon) return 'mdi-magnify'
  // If already a full MDI icon name, use it directly
  if (icon.startsWith('mdi-')) return icon
  const map: Record<string, string> = {
    funding: 'mdi-cash-multiple',
    awareness: 'mdi-bullhorn-outline',
    partnership: 'mdi-handshake-outline',
    collaboration: 'mdi-account-group-outline',
    certification: 'mdi-certificate-outline',
    'tech-funding': 'mdi-laptop',
    cooperative: 'mdi-wheat',
    'chef-hat': 'mdi-chef-hat',
    microscope: 'mdi-microscope',
    coin: 'mdi-currency-usd',
    tool: 'mdi-tools',
  }
  return map[icon] || 'mdi-magnify'
}

const getEmoji = (icon?: string): string => {
  const map: Record<string, string> = {
    funding: '💰',
    awareness: '📢',
    partnership: '🤝',
    collaboration: '👥',
    certification: '📜',
    'tech-funding': '💻',
    cooperative: '🌾',
  }
  return map[icon || ''] || '🔍'
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

/* ── Standalone section ─────────────────────────────────────── */
.project-looking-for {
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

.chips-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}

.chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 11px 16px;
  border-radius: 12px;
  font-size: 0.9375rem;
  font-weight: 500;

  &.tone-0 {
    background: $earth-10;
  }

  &.tone-1 {
    background: $saffron-pale;
  }
}

.chip-emoji {
  font-size: 1.05em;
  flex-shrink: 0;
}

.chip-text {
  min-width: 0;
  word-break: break-word;
}

/* ── Column mode ─────────────────────────────────────────────── */
.needs-column {
  display: flex;
  flex-direction: column;
}

.col-header {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 9px;
}

.col-header-icon {
  width: 20px;
  height: 20px;
  border-radius: 5px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;

  &--warm {
    background: rgba(133, 79, 11, 0.12);
  }
}

.col-header-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;

  &--warm {
    color: #854f0b;
  }
}

.needs-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.need-card {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: $saffron-pale;
  border: 0.5px solid $saffron;
  border-radius: 12px;
  padding: 12px 14px;
}

.need-icon {
  width: 30px;
  height: 30px;
  border-radius: 7px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(133, 79, 11, 0.1);
}

.need-body {
  flex: 1;
  min-width: 0;
}

.need-title {
  font-size: 13px;
  font-weight: 700;
  color: #5a3200;
  margin: 0 0 1px;
  line-height: 1.3;
}

.need-desc {
  font-size: 11px;
  color: #7a5020;
  margin: 0;
  line-height: 1.4;
}
</style>
