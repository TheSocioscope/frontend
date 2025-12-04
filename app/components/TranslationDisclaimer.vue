<template>
  <v-alert
    v-if="showDisclaimer"
    type="info"
    variant="text"
    density="compact"
    class="translation-disclaimer mb-4"
  >
    <div class="d-flex align-center justify-space-between flex-wrap ga-2">
      <div class="text-body-2">
        {{ disclaimerText }}
      </div>
      <v-btn size="small" variant="outlined" @click="$emit('toggleOriginal')">
        {{ buttonText }}
      </v-btn>
    </div>
  </v-alert>
</template>

<script setup lang="ts">
const props = defineProps<{
  originalLang: string
  currentLocale?: string
  showingOriginal?: boolean
}>()

defineEmits<{
  toggleOriginal: []
}>()

const { t, locale } = useI18n()
const { getLanguageName, isTranslated } = useMultilingual()

const currentLocale = computed(() => props.currentLocale || locale.value)

const showDisclaimer = computed(() => {
  // Always show if original language is different from current locale
  return props.originalLang !== locale.value
})

const languageName = computed(() => {
  return getLanguageName(currentLocale.value)
})

const originalLanguageName = computed(() => {
  return getLanguageName(props.originalLang)
})

const disclaimerText = computed(() => {
  if (props.showingOriginal) {
    // Viewing original version
    return t('projects.viewingOriginal', { language: originalLanguageName.value })
  } else {
    // Viewing translated version
    return t('projects.translationDisclaimer', { language: languageName.value })
  }
})

const buttonText = computed(() => {
  if (props.showingOriginal) {
    // Button to go back to translated
    return t('projects.viewTranslated', { language: languageName.value })
  } else {
    // Button to view original
    return t('projects.viewInOriginal', { language: originalLanguageName.value })
  }
})
</script>

<style scoped>
.translation-disclaimer {
  border-left: 3px solid rgba(var(--v-theme-info), 0.5) !important;
}
</style>
