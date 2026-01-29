<template>
  <div v-if="showDisclaimer" class="translation-disclaimer">
    <div class="disclaimer-content">
      <div class="disclaimer-icon">🌐</div>
      <div class="disclaimer-text">
        {{ disclaimerText }}
      </div>
      <button class="disclaimer-button" @click="$emit('toggleOriginal')">
        {{ buttonText }}
      </button>
    </div>
  </div>
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

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.translation-disclaimer {
  background-color: $warm-beige;
  border-left: 4px solid $green-bright;
  padding: 1.25rem 1.5rem;
  margin-bottom: 2rem;
  border-radius: 0;
}

.disclaimer-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.disclaimer-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.disclaimer-text {
  flex: 1;
  min-width: 200px;
  font-family: 'Playfair Display', serif;
  color: $brown-dark;
  line-height: 1.6;
}

.disclaimer-button {
  padding: 0.5rem 1.25rem;
  border: 2px solid $green-bright;
  background-color: transparent;
  color: $brown-dark;
  font-family: 'Playfair Display', serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 4px;
  white-space: nowrap;

  &:hover {
    background-color: $green-bright;
    color: $cream;
  }
}
</style>
