<template>
  <div class="fab-wrapper">
    <div
      class="fab-tray"
      :class="{ open: isOpen }"
      role="menu"
      :aria-label="$t('projects.detail.share')"
    >
      <p class="tray-label">{{ $t('projects.detail.share') }}</p>
      <a :href="facebookShareUrl" target="_blank" rel="noopener noreferrer" class="tray-row" role="menuitem">
        <v-icon size="small" color="#27421d">mdi-facebook</v-icon>
        Facebook
      </a>
      <a :href="linkedinShareUrl" target="_blank" rel="noopener noreferrer" class="tray-row" role="menuitem">
        <v-icon size="small" color="#27421d">mdi-linkedin</v-icon>
        LinkedIn
      </a>
      <a :href="emailShareUrl" class="tray-row" role="menuitem">
        <v-icon size="small" color="#27421d">mdi-email-outline</v-icon>
        Email
      </a>
      <button class="tray-row" role="menuitem" @click="copyLink">
        <v-icon size="small" color="#27421d">mdi-content-copy</v-icon>
        {{ copied ? $t('common.copied') : $t('common.copyLink') }}
      </button>
    </div>
    <button
      class="fab-btn"
      :aria-label="$t('projects.detail.share')"
      :aria-expanded="isOpen"
      @click="isOpen = !isOpen"
    >
      <v-icon size="20">{{ isOpen ? 'mdi-close' : 'mdi-share-variant' }}</v-icon>
    </button>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  projectName: string
  projectUrl: string
}>()

const { t: $t } = useI18n()
const isOpen = ref(false)
const copied = ref(false)

const encodedUrl = computed(() => encodeURIComponent(props.projectUrl))
const encodedTitle = computed(() => encodeURIComponent(props.projectName))

const facebookShareUrl = computed(
  () => `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl.value}`
)
const linkedinShareUrl = computed(
  () => `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl.value}`
)
const emailShareUrl = computed(
  () => `mailto:?subject=${encodedTitle.value}&body=${encodedUrl.value}`
)

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(props.projectUrl)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch {
    // ignore
  }
}

// Close tray when clicking outside
const wrapperEl = ref<HTMLElement | null>(null)
const onOutsideClick = (e: MouseEvent) => {
  if (wrapperEl.value && !wrapperEl.value.contains(e.target as Node)) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('click', onOutsideClick))
onBeforeUnmount(() => document.removeEventListener('click', onOutsideClick))
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.fab-wrapper {
  position: fixed;
  bottom: 5.5rem; /* clears the back-to-top FAB (24px + ~52px btn + 12px gap) */
  right: 1.5rem;
  z-index: $z-dropdown;
}

.fab-btn {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: $green-forest;
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
  transition: background $transition-fast;

  &:hover {
    background: $green-leaf;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 3px;
  }
}

.fab-tray {
  display: none;
  position: absolute;
  bottom: 56px;
  right: 0;
  background: white;
  border: 0.5px solid $border-soft;
  border-radius: 12px;
  padding: 8px;
  min-width: 168px;
  box-shadow: $shadow-md;

  &.open {
    display: block;
  }
}

.tray-label {
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: $text-caption;
  margin: 0 0 6px;
  padding: 0 6px;
}

.tray-row {
  display: flex;
  align-items: center;
  gap: 9px;
  padding: 8px 10px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px;
  font-family: $font-family-base;
  color: $text-primary;
  text-decoration: none;
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  transition: background $transition-fast;

  &:hover {
    background: $earth-5;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: -2px;
    border-radius: 8px;
  }
}
</style>
