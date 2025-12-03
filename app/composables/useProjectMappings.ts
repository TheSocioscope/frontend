export const useProjectMappings = () => {
  const { t, locale } = useI18n()

  const getStatusLabel = (statusKey: string) => {
    return t(`projects.status.${statusKey}`)
  }

  const getContinentLabel = (continentKey: string) => {
    return t(`projects.continents.${continentKey}`)
  }

  const getCountryLabel = (countryKey: string) => {
    return t(`projects.countries.${countryKey}`)
  }

  const getFieldLabel = (fieldKey: string) => {
    return t(`projects.fields.${fieldKey}`)
  }

  const getThematicLabel = (thematicKey: string) => {
    return t(`projects.thematics.${thematicKey}`)
  }

  const getTypeLabel = (typeKey: string) => {
    return t(`projects.types.${typeKey}`)
  }

  const getStateLabel = (stateKey: string) => {
    return t(`projects.state.${stateKey}`)
  }

  const getPeriodicityLabel = (periodicityKey: string) => {
    if (!periodicityKey) return ''
    // Extract the key after "misc.frequency."
    const key = periodicityKey.replace('misc.frequency.', '')
    return t(`projects.misc.frequency.${key}`)
  }

  return {
    getStatusLabel,
    getContinentLabel,
    getCountryLabel,
    getFieldLabel,
    getThematicLabel,
    getTypeLabel,
    getStateLabel,
    getPeriodicityLabel
  }
}
