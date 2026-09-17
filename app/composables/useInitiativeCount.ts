/**
 * Number of initiatives in the projects collection. Shared by every place
 * that shows the count, so it updates automatically when an initiative
 * JSON file is added or removed.
 */
export const useInitiativeCount = async () => {
  const { data } = await useAsyncData('initiative-count', () =>
    queryCollection('projects').count()
  )
  return computed(() => data.value ?? 0)
}
