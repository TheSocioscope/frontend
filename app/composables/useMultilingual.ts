/**
 * Composable for handling multilingual content
 */

export const useMultilingual = () => {
  const { locale } = useI18n()

  /**
   * Get localized text from a multilingual object
   * @param textObj - The multilingual text object or plain string
   * @param originalLang - The original language of the content (optional)
   * @returns The localized text
   */
  const getLocalizedText = (
    textObj: string | Record<string, string> | undefined,
    originalLang?: string
  ): string => {
    // Handle undefined/null
    if (!textObj) return ''

    // If it's already a string, return it
    if (typeof textObj === 'string') return textObj

    // Try to get text in current locale
    if (textObj[locale.value]) {
      return textObj[locale.value]
    }

    // Fallback to original language if provided
    if (originalLang && textObj[originalLang]) {
      return textObj[originalLang]
    }

    // Fallback to English
    if (textObj.en) {
      return textObj.en
    }

    // Last resort: return first available language
    const firstLang = Object.keys(textObj)[0]
    return firstLang ? textObj[firstLang] : ''
  }

  /**
   * Check if the current locale is different from the original language
   * @param originalLang - The original language of the content
   * @returns True if content is being displayed in a translated language
   */
  const isTranslated = (originalLang?: string): boolean => {
    if (!originalLang) return false
    return locale.value !== originalLang
  }

  /**
   * Get the display name of a language code
   * @param langCode - The language code (en, fr, es, de, etc.)
   * @returns The display name of the language
   */
  const getLanguageName = (langCode: string): string => {
    const languageNames: Record<string, Record<string, string>> = {
      en: { en: 'English', fr: 'Anglais', es: 'Inglés', de: 'Englisch' },
      fr: { en: 'French', fr: 'Français', es: 'Francés', de: 'Französisch' },
      es: { en: 'Spanish', fr: 'Espagnol', es: 'Español', de: 'Spanisch' },
      de: { en: 'German', fr: 'Allemand', es: 'Alemán', de: 'Deutsch' },
      it: { en: 'Italian', fr: 'Italien', es: 'Italiano', de: 'Italienisch' },
      pt: { en: 'Portuguese', fr: 'Portugais', es: 'Portugués', de: 'Portugiesisch' },
      pl: { en: 'Polish', fr: 'Polonais', es: 'Polaco', de: 'Polnisch' },
      id: { en: 'Indonesian', fr: 'Indonésien', es: 'Indonesio', de: 'Indonesisch' },
      et: { en: 'Estonian', fr: 'Estonien', es: 'Estonio', de: 'Estnisch' },
      lt: { en: 'Lithuanian', fr: 'Lituanien', es: 'Lituano', de: 'Litauisch' }
    }

    return languageNames[langCode]?.[locale.value] || langCode.toUpperCase()
  }

  return {
    getLocalizedText,
    isTranslated,
    getLanguageName
  }
}
