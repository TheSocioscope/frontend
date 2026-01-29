<template>
  <v-alert v-if="show" type="info" variant="tonal" class="translation-disclaimer" closable>
    <div class="disclaimer-content">
      <v-icon class="mr-2">mdi-translate</v-icon>
      <div class="disclaimer-text">
        <p v-if="!showingOriginal">
          {{ $t('projects.translationDisclaimer', { language: getLanguageName(originalLang) }) }}
        </p>
        <p v-else>
          {{ $t('projects.viewingOriginal', { language: getLanguageName(originalLang) }) }}
        </p>
      </div>
      <v-btn variant="outlined" size="small" class="ml-4" @click="$emit('toggle-language')">
        {{ showingOriginal ? $t('common.viewTranslation') : $t('common.viewOriginal') }}
      </v-btn>
    </div>
  </v-alert>
</template>

<script setup lang="ts">
const props = defineProps<{
  originalLang: string
  currentLocale: string
  showingOriginal: boolean
}>()

defineEmits<{
  'toggle-language': []
}>()

const { t: $t } = useI18n()

const show = computed(() => {
  return props.originalLang && props.originalLang !== props.currentLocale
})

const getLanguageName = (lang: string) => {
  const languages: Record<string, string> = {
    en: 'English',
    fr: 'French',
    es: 'Spanish',
    de: 'German',
    pt: 'Portuguese',
    it: 'Italian',
    zh: 'Chinese',
    ja: 'Japanese',
    ar: 'Arabic',
    ru: 'Russian'
  }
  return languages[lang] || lang.toUpperCase()
}
</script>

<style scoped lang="scss">
.translation-disclaimer {
  margin-bottom: 2rem;
  border-left: 4px solid rgb(var(--v-theme-info));
}

.disclaimer-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  flex-wrap: wrap;
}

.disclaimer-text {
  flex: 1;

  p {
    margin: 0;
    line-height: 1.5;
  }
}

@media (max-width: 768px) {
  .disclaimer-content {
    flex-direction: column;
    align-items: flex-start;
  }

  .ml-4 {
    margin-left: 0 !important;
    width: 100%;
  }
}
</style>
