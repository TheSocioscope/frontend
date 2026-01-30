<template>
  <div v-if="show" class="translation-disclaimer">
    <div class="disclaimer-content">
      <v-icon class="disclaimer-icon">mdi-translate</v-icon>
      <div class="disclaimer-text">
        {{ displayMessage }}
      </div>
      <button class="disclaimer-button" @click="$emit('toggleOriginal')">
        {{ showingOriginal ? $t('common.viewTranslation') : $t('common.viewOriginal') }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  originalLang: string
  showingOriginal?: boolean
}>()

defineEmits<{
  toggleOriginal: []
}>()

const { locale } = useI18n()

const show = computed(() => {
  return props.originalLang && props.originalLang !== locale.value
})

const getLanguageName = (lang: string) => {
  const langKey = `common.languages.${lang}`
  const translated = $t(langKey)
  // If translation key doesn't exist, it returns the key itself, so fallback to uppercase
  return translated === langKey ? lang.toUpperCase() : translated
}

const displayMessage = computed(() => {
  const langName = getLanguageName(props.originalLang)
  const currentLangName = getLanguageName(locale.value)
  if (props.showingOriginal) {
    return $t('projects.viewingOriginal', { language: langName })
  } else {
    return $t('projects.translationDisclaimer', {
      language: langName,
      currentLanguage: currentLangName
    })
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
