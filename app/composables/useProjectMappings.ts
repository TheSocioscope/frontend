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
    const thematics = t('projects.thematics') as any[]
    const thematic = thematics.find((t: any) => t[thematicIndex])
    return thematic ? thematic[thematicIndex] : ''
  }

  const getTypeLabel = (typeIndex: number) => {
    const types = t('projects.types') as any[]
    const type = types.find((t: any) => t[typeIndex])
    return type ? type[typeIndex] : ''
  }

  const getStateLabel = (stateValue: number) => {
    const states = t('projects.state') as any[]
    const state = states.find((s: any) => s[stateValue])
    return state ? state[stateValue] : ''
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
