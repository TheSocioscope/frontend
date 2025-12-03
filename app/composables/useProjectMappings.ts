export const useProjectMappings = () => {
  const { t, locale } = useI18n()

  const getStatusLabel = (statusValue: number) => {
    return t(`projects.status.${statusValue}`)
  }

  const getContinentLabel = (continentValue: number) => {
    return t(`projects.continents.${continentValue}`)
  }

  const getCountryLabel = (countryValue: number) => {
    return t(`projects.countries.${countryValue}`)
  }

  const getFieldLabel = (fieldValue: number) => {
    return t(`projects.fields.${fieldValue}`)
  }

  const getThematicLabel = (thematicIndex: number) => {
    // Vue i18n converts arrays to objects, so access via index
    return t(`projects.thematics.${thematicIndex}.${thematicIndex}`)
  }

  const getTypeLabel = (typeIndex: number) => {
    // Vue i18n converts arrays to objects, so access via index
    return t(`projects.types.${typeIndex}.${typeIndex}`)
  }

  const getStateLabel = (stateValue: number) => {
    // Vue i18n converts arrays to objects, so access via index
    return t(`projects.state.${stateValue}.${stateValue}`)
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
