/**
 * Composable for fetching localized content collections with pagination and sorting
 *
 * @param collection - The collection name (products, resources, faq)
 * @param options - Configuration options
 * @returns Paginated and sorted collection data with reactive state
 */
export const useLocalizedCollection = <T = any>(
  collection: 'products' | 'resources' | 'faq',
  options: {
    /** Number of items per page */
    itemsPerPage?: Ref<number> | number
    /** Current page number (1-indexed) */
    page?: Ref<number> | number
    /** Sort field */
    sortBy?: Ref<string> | string
    /** Sort direction */
    sortOrder?: Ref<'asc' | 'desc'> | 'asc' | 'desc'
    /** Filter published items only */
    publishedOnly?: boolean
  } = {}
) => {
  const { locale } = useI18n()
  const route = useRoute()
  const router = useRouter()

  // Reactive pagination state
  const itemsPerPage = ref(toValue(options.itemsPerPage) || 20)
  const currentPage = ref(toValue(options.page) || 1)
  const sortBy = ref(toValue(options.sortBy) || 'order')
  const sortOrder = ref<'asc' | 'desc'>(toValue(options.sortOrder) || 'asc')

  // Sync with URL query params
  onMounted(() => {
    if (route.query.page) {
      const page = parseInt(route.query.page as string)
      if (!isNaN(page) && page > 0) {
        currentPage.value = page
      }
    }
    if (route.query.perPage) {
      const perPage = parseInt(route.query.perPage as string)
      if (!isNaN(perPage) && perPage > 0) {
        itemsPerPage.value = perPage
      }
    }
    if (route.query.sortBy) {
      sortBy.value = route.query.sortBy as string
    }
    if (route.query.sortOrder && ['asc', 'desc'].includes(route.query.sortOrder as string)) {
      sortOrder.value = route.query.sortOrder as 'asc' | 'desc'
    }
  })

  // Update URL when pagination/sort changes
  watch([currentPage, itemsPerPage, sortBy, sortOrder], () => {
    const query: Record<string, string> = { ...route.query }

    if (currentPage.value > 1) {
      query.page = currentPage.value.toString()
    } else {
      delete query.page
    }

    if (itemsPerPage.value !== 20) {
      query.perPage = itemsPerPage.value.toString()
    } else {
      delete query.perPage
    }

    if (sortBy.value !== 'order') {
      query.sortBy = sortBy.value
    } else {
      delete query.sortBy
    }

    if (sortOrder.value !== 'asc') {
      query.sortOrder = sortOrder.value
    } else {
      delete query.sortOrder
    }

    router.push({ query })
  })

  // Fetch all items for the current locale
  const {
    data: allItems,
    pending,
    error,
    refresh
  } = useAsyncData(
    `${collection}-${locale.value}`,
    async () => {
      const pathPrefix = `/${collection}/${locale.value}/%`

      const items = await queryCollection(collection).where('path', 'LIKE', pathPrefix).all()

      return items as T[]
    },
    { watch: [locale] }
  )

  // Filter and sort items
  const filteredItems = computed(() => {
    if (!allItems.value) return []

    let items = [...allItems.value]

    // Filter published items
    if (options.publishedOnly !== false) {
      items = items.filter((item: any) => item.published !== false)
    }

    // Sort items
    items.sort((a: any, b: any) => {
      const aVal = a[sortBy.value]
      const bVal = b[sortBy.value]

      if (aVal === bVal) return 0

      const comparison = aVal < bVal ? -1 : 1
      return sortOrder.value === 'asc' ? comparison : -comparison
    })

    return items
  })

  // Pagination
  const totalItems = computed(() => filteredItems.value.length)
  const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage.value))

  const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage.value
    const end = start + itemsPerPage.value
    return filteredItems.value.slice(start, end)
  })

  // Pagination controls
  const hasNextPage = computed(() => currentPage.value < totalPages.value)
  const hasPrevPage = computed(() => currentPage.value > 1)

  const goToPage = (page: number) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  const nextPage = () => {
    if (hasNextPage.value) {
      currentPage.value++
    }
  }

  const prevPage = () => {
    if (hasPrevPage.value) {
      currentPage.value--
    }
  }

  // Infinite scroll support (mobile)
  const displayedItems = ref<T[]>([])
  const hasMore = ref(true)

  const loadMore = () => {
    if (!filteredItems.value) return

    const currentLength = displayedItems.value.length
    const nextBatch = filteredItems.value.slice(currentLength, currentLength + itemsPerPage.value)

    displayedItems.value.push(...nextBatch)
    hasMore.value = displayedItems.value.length < filteredItems.value.length
  }

  // Reset displayed items when filters change
  watch(
    [filteredItems, locale],
    () => {
      displayedItems.value = filteredItems.value.slice(0, itemsPerPage.value)
      hasMore.value = displayedItems.value.length < filteredItems.value.length
    },
    { immediate: true }
  )

  return {
    // Data
    items: paginatedItems,
    allItems: filteredItems,
    pending,
    error,
    refresh,

    // Pagination state
    currentPage,
    totalItems,
    totalPages,
    itemsPerPage,

    // Pagination actions
    goToPage,
    nextPage,
    prevPage,
    hasNextPage,
    hasPrevPage,

    // Sorting
    sortBy,
    sortOrder,

    // Infinite scroll (mobile)
    displayedItems,
    loadMore,
    hasMore
  }
}
