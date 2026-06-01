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
      <button
        v-for="(item, index) in localizedLookingFor"
        :key="index"
        class="need-card need-card--link"
        @click="emit('connect')"
      >
        <div class="need-icon" aria-hidden="true">
          <v-icon size="small" color="#854F0B">{{ getMdiIcon(item.icon) }}</v-icon>
        </div>
        <div class="need-body">
          <p class="need-title">{{ item.title }}</p>
          <p v-if="item.description" class="need-desc">{{ item.description }}</p>
        </div>
        <v-icon class="need-link-icon" size="14">mdi-email-outline</v-icon>
      </button>
    </div>
  </div>

  <!-- Standalone section mode (default) -->
  <section v-else id="looking-for" class="project-looking-for">
    <span class="section-label">{{ $t('projects.detail.lookingFor') }}</span>
    <div class="needs-list">
      <button
        v-for="(item, index) in localizedLookingFor"
        :key="index"
        class="need-card need-card--link"
        @click="emit('connect')"
      >
        <div class="need-icon" aria-hidden="true">
          <v-icon size="small" color="#854F0B">{{ getMdiIcon(item.icon) }}</v-icon>
        </div>
        <div class="need-body">
          <h3 class="need-title">{{ item.title }}</h3>
          <p v-if="item.description" class="need-desc">{{ item.description }}</p>
        </div>
        <v-icon class="need-link-icon" size="14">mdi-email-outline</v-icon>
      </button>
    </div>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  localizedLookingFor: Array<{ title: string; description?: string; icon?: string }>
  column?: boolean
}>()

const emit = defineEmits<{ connect: [] }>()

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

/* ── Column mode header ─────────────────────────────────────── */
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

/* ── Shared list + cards ────────────────────────────────────── */
.needs-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.need-card {
  display: flex;
  align-items: center;
  gap: 12px;
  background: $saffron-pale;
  border: 0.5px solid $saffron;
  border-radius: 12px;
  padding: 12px 14px;
  text-decoration: none;

  /* Clickable card: pointer + hover lift */
  &--link {
    cursor: pointer;
    width: 100%;
    text-align: left;
    font-family: $font-family-base;
    font-size: inherit;
    appearance: none;
    transition:
      background $transition-fast,
      border-color $transition-fast,
      box-shadow $transition-fast,
      transform $transition-fast;

    &:hover {
      background: rgba(133, 79, 11, 0.1);
      border-color: rgba(133, 79, 11, 0.45);
      box-shadow: 0 2px 8px rgba(133, 79, 11, 0.1);
      transform: translateY(-1px);

      .need-link-icon {
        opacity: 1;
      }
    }

    &:focus-visible {
      outline: 2px solid #854f0b;
      outline-offset: 2px;
    }
  }
}

.need-icon {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(133, 79, 11, 0.15);
}

.need-body {
  flex: 1;
  min-width: 0;
}

.need-title {
  font-size: 13px;
  font-weight: 600;
  color: #5a3200;
  margin: 0;
  line-height: 1.4;
}

.need-desc {
  font-size: 11px;
  color: #7a5020;
  margin: 0;
  line-height: 1.4;
}

/* Contact indicator — always subtly visible, brighter on hover */
.need-link-icon {
  color: #854f0b;
  opacity: 0.4;
  flex-shrink: 0;
  transition: opacity $transition-fast;
}

.need-card--link:hover .need-link-icon {
  opacity: 1;
}
</style>
