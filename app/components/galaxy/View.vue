<template>
  <section
    ref="rootEl"
    class="galaxy-view"
    :aria-label="$t('galaxy.regionLabel', 'Initiatives ecosystem')"
  >
    <div v-if="errorMessage" class="galaxy-state">
      <v-icon color="error" size="40">mdi-alert-circle-outline</v-icon>
      <p>{{ $t('galaxy.loadError', 'Failed to load the galaxy.') }}</p>
      <small>{{ errorMessage }}</small>
    </div>

    <div v-else-if="!data" class="galaxy-state">
      <v-progress-circular indeterminate size="32" />
      <p>{{ $t('galaxy.loading', 'Loading the ecosystem…') }}</p>
    </div>

    <template v-else>
      <GalaxyCanvas
        :nodes="data.nodes"
        :domain="data.domain"
        :continent-colors="data.continentColors"
        :visible-ids="effectiveVisibleSet"
        @hover="onHover"
        @select="onSelect"
      />
      <GalaxySearch :nodes="data.nodes" @match="onSearchMatch" />
      <GalaxyLegend
        :continent-colors="data.continentColors"
        :present-continents="presentContinents"
      />
      <GalaxyOverlay
        :payload="hoverPayload"
        :continent-colors="data.continentColors"
        :parent-rect="parentRect"
      />
      <GalaxySheet
        v-model="sheetOpen"
        :node="sheetNode"
        :continent-colors="data.continentColors"
      />
      <GalaxyA11yList :nodes="a11yNodes" />

      <GalaxyEmpty
        v-if="effectiveVisibleSet && effectiveVisibleSet.size === 0"
        :can-reset="Boolean(visibleIds) || searchedIds !== null"
        @reset="onResetAll"
      />
    </template>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  // Optional: when present, nodes outside this set fade to 0.15 opacity.
  // Pass null/undefined to render every node at full opacity.
  visibleIds?: number[] | null
}>()

const emit = defineEmits<{
  reset: []
}>()

const { t: $t } = useI18n()
const localePath = useLocalePath()
const router = useRouter()

const data = ref<GalaxyData | null>(null)
const errorMessage = ref<string | null>(null)
const rootEl = ref<HTMLElement | null>(null)
const parentRect = ref<DOMRect | null>(null)
const hoverPayload = ref<{ node: GalaxyNode; clientX: number; clientY: number } | null>(null)
const sheetOpen = ref(false)
const sheetNode = ref<GalaxyNode | null>(null)

const filterIdSet = computed<Set<number> | null>(() => {
  if (!props.visibleIds) return null
  return new Set(props.visibleIds)
})

// Search-result ids; null when search is empty.
const searchedIds = ref<number[] | null>(null)
const searchIdSet = computed<Set<number> | null>(() => {
  if (!searchedIds.value) return null
  return new Set(searchedIds.value)
})

// Effective visible set = filter ∩ search. Either condition narrows the set;
// passing null to the canvas means "show everything at full opacity."
const effectiveVisibleSet = computed<Set<number> | null>(() => {
  const f = filterIdSet.value
  const s = searchIdSet.value
  if (!f && !s) return null
  if (f && !s) return f
  if (!f && s) return s
  // both present — intersection
  const out = new Set<number>()
  for (const id of s!) if (f!.has(id)) out.add(id)
  return out
})

// Pare the a11y list to currently-visible nodes so screen-reader users
// don't read 600+ entries when filters are applied.
const a11yNodes = computed<GalaxyNode[]>(() => {
  if (!data.value) return []
  const v = effectiveVisibleSet.value
  if (!v) return data.value.nodes
  return data.value.nodes.filter((n) => v.has(n.id))
})

const presentContinents = computed<string[]>(() => {
  if (!data.value) return []
  const set = new Set<string>()
  for (const n of data.value.nodes) set.add(n.continent)
  return [...set]
})

const onSearchMatch = (ids: number[] | null) => {
  searchedIds.value = ids
}

const onResetAll = () => {
  searchedIds.value = null
  emit('reset')
}

const isMobileViewport = () =>
  typeof window !== 'undefined' && window.matchMedia('(max-width: 767px)').matches

let resizeObserver: ResizeObserver | null = null

const updateRect = () => {
  if (rootEl.value) parentRect.value = rootEl.value.getBoundingClientRect()
}

const onHover = (payload: { node: GalaxyNode; clientX: number; clientY: number } | null) => {
  hoverPayload.value = payload
  // Refresh rect on each hover so the tooltip stays correctly positioned even
  // after page scroll without paying ResizeObserver overhead.
  if (payload) updateRect()
}

const onSelect = (node: GalaxyNode) => {
  if (isMobileViewport()) {
    sheetNode.value = node
    sheetOpen.value = true
  } else {
    router.push(localePath(`/projects/${node.slug}`))
  }
}

onMounted(async () => {
  if (typeof window === 'undefined') return

  // Observe size changes for tooltip positioning math.
  resizeObserver = new ResizeObserver(updateRect)
  if (rootEl.value) resizeObserver.observe(rootEl.value)
  window.addEventListener('scroll', updateRect, { passive: true })
  updateRect()

  try {
    const baseURL = useRuntimeConfig().app.baseURL || '/'
    const url = `${baseURL.replace(/\/$/, '')}/data/galaxy-positions.json`
    const res = await fetch(url)
    if (!res.ok) throw new Error(`HTTP ${res.status}`)
    data.value = (await res.json()) as GalaxyData
  } catch (e: unknown) {
    errorMessage.value = e instanceof Error ? e.message : String(e)
  }
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  resizeObserver = null
  if (typeof window !== 'undefined') {
    window.removeEventListener('scroll', updateRect)
  }
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.galaxy-view {
  position: relative;
  width: 100%;
  height: $galaxy-canvas-min-h-desktop;
  min-height: 480px;
  overflow: hidden;
  border-radius: 12px;

  @media (max-width: $breakpoint-md - 1) {
    height: $galaxy-canvas-min-h-tablet;
  }

  @media (max-width: $breakpoint-sm - 1) {
    height: $galaxy-canvas-min-h-mobile;
    border-radius: 0;
  }
}

.galaxy-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: $spacing-sm;
  padding: $spacing-md;
  color: rgba(0, 0, 0, 0.6);
  text-align: center;

  small {
    color: rgba(0, 0, 0, 0.45);
  }
}
</style>
