<template>
  <div class="projects-map">
    <div ref="mapWrap" class="map-wrap">
      <svg ref="svgEl" class="world-map" />
      <div
        v-if="hovered && supportsHover"
        class="map-tooltip"
        :style="{ left: tooltipX + 'px', top: tooltipY + 'px' }"
      >
        <div class="tt-name">{{ hovered.name }}</div>
        <div class="tt-count">
          <strong>{{ hovered.count }}</strong>
          {{ $t('projects.projectsFound') }}
        </div>
      </div>

      <div v-if="loading" class="map-state">
        <v-progress-circular indeterminate size="32" />
      </div>
      <div v-else-if="emptyState" class="map-state">
        <v-icon size="40" color="primary">mdi-filter-off-outline</v-icon>
        <p>{{ $t('projects.noProjects', 'No projects match these filters') }}</p>
      </div>

      <!-- Zoom controls — pinch + scroll work natively, these surface
           the same actions as tappable buttons on mobile. -->
      <div v-if="!loading && !emptyState" class="map-controls">
        <button
          type="button"
          class="map-btn"
          :aria-label="$t('projects.zoomIn', 'Zoom in')"
          @click="zoomBy(1.5)"
        >
          <v-icon size="small">mdi-plus</v-icon>
        </button>
        <button
          type="button"
          class="map-btn"
          :aria-label="$t('projects.zoomOut', 'Zoom out')"
          @click="zoomBy(1 / 1.5)"
        >
          <v-icon size="small">mdi-minus</v-icon>
        </button>
        <button
          type="button"
          class="map-btn"
          :aria-label="$t('projects.resetZoom', 'Reset zoom')"
          @click="resetZoom"
        >
          <v-icon size="small">mdi-image-filter-center-focus</v-icon>
        </button>
      </div>
    </div>

    <!-- Compact horizontal legend below the map (was floating bottom-right
         which crowded the map on phones). -->
    <div v-if="!loading && !emptyState" class="map-legend" aria-hidden="true">
      <span class="legend-label">{{ $t('projects.legend.fewer', 'Fewer') }}</span>
      <div class="legend-steps">
        <span
          v-for="step in legendSteps"
          :key="step.label"
          class="legend-swatch"
          :style="{ background: step.color }"
          :title="step.label"
        />
      </div>
      <span class="legend-label">{{ $t('projects.legend.more', 'More') }}</span>
    </div>

    <!-- Country preview sheet — appears when a user taps a country on
         touch devices (desktop already gets a hover tooltip). Decouples
         "explore" from "commit" so users can preview before filtering. -->
    <Teleport to="body">
      <Transition name="preview-fade">
        <div
          v-if="previewCountry"
          class="preview-backdrop"
          @click="closePreview"
        />
      </Transition>
      <Transition name="preview-sheet">
        <aside
          v-if="previewCountry"
          class="preview-sheet"
          role="dialog"
          aria-modal="true"
          :aria-label="$t('projects.preview.title', 'Country preview')"
        >
          <header class="preview-header">
            <div class="preview-titles">
              <span class="preview-eyebrow">
                {{ $t('projects.preview.eyebrow', 'Country') }}
              </span>
              <h3 class="preview-name">
                {{ getCountryLabel(previewCountry.code) || previewCountry.name }}
              </h3>
            </div>
            <button
              type="button"
              class="preview-close"
              :aria-label="$t('common.close', 'Close')"
              @click="closePreview"
            >
              <v-icon>mdi-close</v-icon>
            </button>
          </header>
          <div class="preview-body">
            <div class="preview-count">
              <span class="preview-count-num">{{ previewCountry.count }}</span>
              <span class="preview-count-label">
                {{ $t('projects.projectsFound') }}
              </span>
            </div>
          </div>
          <footer class="preview-actions">
            <button type="button" class="preview-btn-secondary" @click="closePreview">
              {{ $t('common.close', 'Close') }}
            </button>
            <button
              type="button"
              class="preview-btn-primary"
              @click="confirmPreview"
            >
              {{ $t('projects.preview.viewProjects', 'View projects') }}
              <v-icon size="small">mdi-arrow-right</v-icon>
            </button>
          </footer>
        </aside>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { feature } from 'topojson-client'

interface CountryStatsEntry {
  count: number
  projects: Array<{ pubId: number; name: string }>
}

interface SourceProject {
  pubId: number
  country?: string[]
}

const props = defineProps<{
  // Pub-ids of projects matching the current filter set. Map intensity is
  // computed from the intersection of these with content/projects's country
  // arrays.
  filteredIds: number[]
}>()

const emit = defineEmits<{
  selectCountry: [code: string]
}>()

const { t: $t } = useI18n()
const { countryCodeToMapName, getCountryCode } = useCountryMapping()
const { getCountryLabel } = useProjectMappings()
const config = useRuntimeConfig()

const mapWrap = ref<HTMLElement | null>(null)
const svgEl = ref<SVGElement | null>(null)

// Source data — country-stats.json is already produced by
// generate-country-stats.ts and lists every project per country.
const stats = ref<Record<string, CountryStatsEntry>>({})
const loading = ref(true)

// Visible (filtered) count per country — recomputed when filteredIds changes.
const visibleCountByCountryCode = computed<Record<string, number>>(() => {
  const set = new Set(props.filteredIds)
  const out: Record<string, number> = {}
  for (const [code, entry] of Object.entries(stats.value)) {
    let count = 0
    for (const p of entry.projects) {
      if (set.has(p.pubId)) count++
    }
    if (count > 0) out[code] = count
  }
  return out
})

// Same data keyed by topojson country name (for the SVG path lookup).
const visibleCountByMapName = computed<Record<string, number>>(() => {
  const out: Record<string, number> = {}
  for (const [code, count] of Object.entries(visibleCountByCountryCode.value)) {
    const mapName = countryCodeToMapName[code]
    if (mapName) out[mapName] = count
  }
  return out
})

const emptyState = computed(
  () => !loading.value && Object.keys(visibleCountByMapName.value).length === 0
)

// Stepped color scale — 6 buckets matches the homepage map convention.
const COLORS = ['#e8efe7', '#c7dfc6', '#94c692', '#5fa85f', '#3a8c3a', '#1f6f23']
const THRESHOLDS = [1, 5, 15, 30, 60, 100]

const colorFor = (count: number | undefined): string => {
  if (!count || count <= 0) return '#f0f0f0'
  for (let i = THRESHOLDS.length - 1; i >= 0; i--) {
    if (count >= THRESHOLDS[i]) return COLORS[i]
  }
  return COLORS[0]
}

const legendSteps = computed(() => {
  const out: { label: string; color: string }[] = []
  for (let i = 0; i < THRESHOLDS.length; i++) {
    const lower = THRESHOLDS[i]
    const upper = i < THRESHOLDS.length - 1 ? THRESHOLDS[i + 1] - 1 : null
    out.push({
      label: upper ? `${lower}–${upper}` : `${lower}+`,
      color: COLORS[i]
    })
  }
  return out
})

const hovered = ref<{ name: string; count: number; code: string } | null>(null)
const tooltipX = ref(0)
const tooltipY = ref(0)

// Tap-to-preview state — the country preview sheet appears when a user
// taps any country (touch) so they can confirm before committing to a
// filter. Desktop hover tooltip stays as it was.
const previewCountry = ref<{ name: string; count: number; code: string } | null>(null)
const supportsHover = ref(true)

const openPreview = (name: string, count: number, code: string) => {
  previewCountry.value = { name, count, code }
}

const closePreview = () => {
  previewCountry.value = null
}

const confirmPreview = () => {
  if (previewCountry.value) {
    emit('selectCountry', previewCountry.value.code)
    previewCountry.value = null
  }
}


let svg: d3.Selection<SVGElement, unknown, null, undefined> | null = null
let zoomGroup: d3.Selection<SVGGElement, unknown, null, undefined> | null = null
let zoomBehavior: d3.ZoomBehavior<SVGElement, unknown> | null = null
let countriesData: GeoJSON.FeatureCollection | null = null
let resizeObserver: ResizeObserver | null = null
// Last-rendered dimensions — used by zoomToCountry to compute the bounds
// transform after render finishes.
let mapWidth = 0
let mapHeight = 0
let activeProjection: d3.GeoProjection | null = null

const reducedMotion = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

const renderMap = () => {
  if (!svgEl.value || !mapWrap.value || !countriesData) return

  const width = mapWrap.value.clientWidth
  // Responsive height: ~55% of width, clamped between 280 and 560.
  const height = Math.min(560, Math.max(280, Math.round(width * 0.55)))
  mapWidth = width
  mapHeight = height

  svg = d3.select(svgEl.value as SVGElement)
  svg.selectAll('*').remove()
  svg
    .attr('viewBox', `0 0 ${width} ${height}`)
    .attr('preserveAspectRatio', 'xMidYMid meet')
    .style('width', '100%')
    .style('height', `${height}px`)

  const projection = d3
    .geoNaturalEarth1()
    .fitSize([width, height], countriesData as never)
  activeProjection = projection

  const path = d3.geoPath().projection(projection)
  const counts = visibleCountByMapName.value

  // All map paths live inside a single <g> so d3-zoom can transform them
  // together. Without this, zoom would only translate the SVG element
  // and not scale the geography.
  zoomGroup = svg.append('g').attr('class', 'map-zoom')

  zoomGroup
    .selectAll('path')
    .data(countriesData.features)
    .join('path')
    .attr('class', 'country')
    .attr('d', path as never)
    .attr('fill', (d: GeoJSON.Feature) => {
      const name = (d.properties as { name?: string })?.name ?? ''
      return colorFor(counts[name])
    })
    .attr('stroke', '#fff')
    .attr('stroke-width', 0.6)
    .style('cursor', (d: GeoJSON.Feature) => {
      const name = (d.properties as { name?: string })?.name ?? ''
      return counts[name] ? 'pointer' : 'default'
    })
    .on('mousemove', function (this: SVGPathElement, event: MouseEvent, d: GeoJSON.Feature) {
      const name = (d.properties as { name?: string })?.name ?? ''
      const count = counts[name]
      if (!count) {
        hovered.value = null
        return
      }
      d3.select(this).attr('stroke', '#27421d').attr('stroke-width', 1.5)
      const code = getCountryCode(name) ?? ''
      hovered.value = { name, count, code }
      updateTooltipPosition(event)
    })
    .on('mouseout', function (this: SVGPathElement) {
      d3.select(this).attr('stroke', '#fff').attr('stroke-width', 0.6)
      hovered.value = null
    })
    .on('click', function (_e: MouseEvent, d: GeoJSON.Feature) {
      const name = (d.properties as { name?: string })?.name ?? ''
      const count = counts[name]
      if (!count) return
      const code = getCountryCode(name) ?? ''
      // Touch / no-hover devices: open the preview sheet so the user can
      // confirm before committing to the filter. Desktop (hover-capable)
      // already had a tooltip, so a click goes straight through.
      if (supportsHover.value) {
        if (code) emit('selectCountry', code)
      } else {
        openPreview(name, count, code)
      }
    })

  // Wire up zoom behaviour. scaleExtent caps how far in/out the user
  // can go (1x = fit-to-view; 8x = country-level detail).
  zoomBehavior = d3
    .zoom<SVGElement, unknown>()
    .scaleExtent([1, 8])
    .on('zoom', (event) => {
      zoomGroup?.attr('transform', event.transform.toString())
      // Counter-scale stroke widths so borders don't fatten as you zoom.
      zoomGroup
        ?.selectAll<SVGPathElement, unknown>('path.country')
        .attr('stroke-width', 0.6 / event.transform.k)
    })
  svg.call(zoomBehavior as never)
}

const zoomBy = (factor: number) => {
  if (!svg || !zoomBehavior) return
  const sel = svg as d3.Selection<SVGElement, unknown, null, undefined>
  if (reducedMotion()) {
    zoomBehavior.scaleBy(sel, factor)
  } else {
    zoomBehavior.scaleBy(sel.transition().duration(220) as never, factor)
  }
}

const resetZoom = () => {
  if (!svg || !zoomBehavior) return
  const sel = svg as d3.Selection<SVGElement, unknown, null, undefined>
  if (reducedMotion()) {
    zoomBehavior.transform(sel, d3.zoomIdentity)
  } else {
    zoomBehavior.transform(sel.transition().duration(280) as never, d3.zoomIdentity)
  }
}

// Zoom + pan the map to fit a country's bounding box. Called by the
// sidebar when the user clicks a country row — gives the OWID Conflict
// Data Explorer feel where the map responds to sidebar clicks.
const zoomToCountry = (code: string) => {
  if (!svg || !zoomBehavior || !countriesData || !activeProjection) return
  const mapName = countryCodeToMapName[code]
  if (!mapName) return
  const featureMatch = (countriesData.features as GeoJSON.Feature[]).find(
    (f) => (f.properties as { name?: string })?.name === mapName
  )
  if (!featureMatch) return

  const path = d3.geoPath().projection(activeProjection)
  const [[x0, y0], [x1, y1]] = path.bounds(featureMatch)
  const dx = Math.max(x1 - x0, 1)
  const dy = Math.max(y1 - y0, 1)
  const cx = (x0 + x1) / 2
  const cy = (y0 + y1) / 2
  // Fit the country to ~70% of the viewport for visual breathing room.
  const scale = Math.max(1.5, Math.min(8, 0.7 / Math.max(dx / mapWidth, dy / mapHeight)))
  const translate: [number, number] = [
    mapWidth / 2 - scale * cx,
    mapHeight / 2 - scale * cy
  ]
  const transform = d3.zoomIdentity.translate(translate[0], translate[1]).scale(scale)
  const sel = svg as d3.Selection<SVGElement, unknown, null, undefined>

  if (reducedMotion()) {
    zoomBehavior.transform(sel, transform)
  } else {
    zoomBehavior.transform(sel.transition().duration(700) as never, transform)
  }
}

defineExpose({ zoomToCountry, resetZoom, zoomBy })

const updateTooltipPosition = (e: MouseEvent) => {
  if (!mapWrap.value) return
  const rect = mapWrap.value.getBoundingClientRect()
  // Anchor offset from cursor; flip to the left if it would overflow the wrap.
  const TOOLTIP_W = 200
  const lx = e.clientX - rect.left + 14
  tooltipX.value = lx + TOOLTIP_W > rect.width ? lx - TOOLTIP_W - 28 : lx
  tooltipY.value = e.clientY - rect.top - 12
}

onMounted(async () => {
  if (typeof window === 'undefined') return
  supportsHover.value = window.matchMedia('(hover: hover)').matches
  try {
    const baseURL = config.app.baseURL || '/'
    const [statsRes, atlas] = await Promise.all([
      fetch(`${baseURL.replace(/\/$/, '')}/data/country-stats.json`).then((r) => r.json()),
      fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json').then((r) => r.json())
    ])
    stats.value = statsRes
    countriesData = feature(atlas, atlas.objects.countries) as GeoJSON.FeatureCollection
    loading.value = false
    await nextTick()
    renderMap()
    resizeObserver = new ResizeObserver(() => renderMap())
    if (mapWrap.value) resizeObserver.observe(mapWrap.value)
  } catch (e) {
    console.error('Error loading map data:', e)
    loading.value = false
  }
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  resizeObserver = null
})

// Repaint on filter change (positions stay; only fill colors change).
watch(visibleCountByMapName, () => {
  if (!svg || !countriesData) return
  const counts = visibleCountByMapName.value
  svg
    .selectAll<SVGPathElement, GeoJSON.Feature>('path.country')
    .attr('fill', (d) => {
      const name = (d.properties as { name?: string })?.name ?? ''
      return colorFor(counts[name])
    })
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.projects-map {
  position: relative;
  width: 100%;
  background: white;
  border: 1px solid $border-soft;
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.875rem;

  @media (max-width: 600px) {
    padding: 0.75rem;
    gap: 0.625rem;
  }
}

.map-wrap {
  position: relative;
  width: 100%;
  min-height: 280px;
}


.world-map {
  display: block;
  width: 100%;
}

.map-tooltip {
  position: absolute;
  background: white;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid $border-soft;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);
  font-size: 0.8125rem;
  pointer-events: none;
  z-index: 5;
  width: 200px;

  .tt-name {
    font-weight: 600;
    color: $green-dark;
    margin-bottom: 2px;
  }

  .tt-count {
    color: $text-secondary;

    strong {
      color: $green-dark;
      font-weight: 700;
    }
  }
}

.map-state {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: $text-caption;
  text-align: center;
}

/* Compact legend strip below the map — gradient-style with "Fewer" /
   "More" labels at the ends so it reads at a glance without forcing the
   user to parse number ranges. */
.map-legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.6875rem;
  color: $text-caption;
}

.legend-label {
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
}

.legend-steps {
  display: flex;
  border: 1px solid $border-soft;
  border-radius: 4px;
  overflow: hidden;
}

.legend-swatch {
  width: 22px;
  height: 10px;
  display: block;

  @media (max-width: 600px) {
    width: 28px;
    height: 12px;
  }
}

.country.country {
  transition: fill 0.15s, stroke 0.15s;
}

/* Zoom controls — fixed bottom-left so they don't overlap the
   bottom-right legend. Stacked vertically on a small surface. */
.map-controls {
  position: absolute;
  left: 12px;
  bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 2;

  @media (max-width: 600px) {
    /* Tighter on phone, but stay floating so they're always reachable */
    left: 8px;
    bottom: 8px;
  }
}

.map-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  background: rgba(255, 255, 255, 0.96);
  border: 1px solid $border-soft;
  border-radius: 6px;
  color: $text-secondary;
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);

  &:hover {
    background: white;
    color: $green-forest;
    border-color: $green-leaf;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
    z-index: 1;
  }

  &:active {
    background: $earth-10;
  }

  /* Mobile: 44px buttons (Apple HIG min) for thumb-friendly tapping. */
  @media (max-width: 600px) {
    width: 44px;
    height: 44px;
    border-radius: 8px;
  }
}

@media (max-width: 600px) {
  /* Move zoom controls to bottom-right on phone so they sit further from
     the natural left-thumb resting position when scrolling. The legend
     now sits below the map (not corner-floated) so the corner is free. */
  .map-controls {
    left: auto;
    right: 8px;
  }
}

/* === Country preview sheet (touch devices) === */

.preview-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(44, 36, 22, 0.4);
  backdrop-filter: blur(2px);
  z-index: 1100;
}

.preview-sheet {
  position: fixed;
  left: 50%;
  bottom: 1rem;
  transform: translateX(-50%);
  width: calc(100% - 2rem);
  max-width: 460px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.18);
  z-index: 1101;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  font-family: $font-family-base;

  @media (min-width: 768px) {
    /* On rare desktop touch surfaces (Surface, etc.) keep it as a centred
       modal-style sheet rather than bottom-anchored. */
    bottom: auto;
    top: 50%;
    transform: translate(-50%, -50%);
  }
}

.preview-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.75rem;
  padding: 1rem 1rem 0.5rem;
}

.preview-titles {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
}

.preview-eyebrow {
  font-size: 0.625rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: $text-caption;
  font-weight: 700;
}

.preview-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: $brown-dark;
  margin: 0;
  line-height: 1.25;
}

.preview-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border: none;
  background: $earth-10;
  border-radius: 999px;
  color: $brown-dark;
  cursor: pointer;
  flex-shrink: 0;

  &:hover {
    background: $earth-15;
  }
  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }
}

.preview-body {
  padding: 0.5rem 1rem 1rem;
}

.preview-count {
  display: flex;
  align-items: baseline;
  gap: 0.5rem;
  padding: 0.875rem 1rem;
  background: rgba(76, 160, 73, 0.08);
  border-left: 3px solid $green-bright;
  border-radius: 4px;
}

.preview-count-num {
  font-size: 1.75rem;
  font-weight: 800;
  color: $green-dark;
  line-height: 1;
}

.preview-count-label {
  font-size: 0.875rem;
  color: $brown-dark;
  opacity: 0.85;
}

.preview-actions {
  display: flex;
  gap: 0.625rem;
  padding: 0.75rem 1rem 1rem;
  border-top: 1px solid $border-soft;
  background: $surface-cream;
}

.preview-btn-secondary,
.preview-btn-primary {
  flex: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.375rem;
  height: 44px;
  border-radius: 6px;
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s, color 0.15s;
}

.preview-btn-secondary {
  background: white;
  color: $brown-dark;
  border: 1px solid $border-soft;

  &:hover {
    border-color: $brown-dark;
  }
  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }
}

.preview-btn-primary {
  background: $green-bright;
  color: white;
  border: 1px solid $green-bright;

  &:hover {
    background: $green-forest;
    border-color: $green-forest;
  }
  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
  }
}

/* Preview sheet enter/leave animations */
.preview-fade-enter-active,
.preview-fade-leave-active {
  transition: opacity 0.18s ease;
}
.preview-fade-enter-from,
.preview-fade-leave-to {
  opacity: 0;
}

.preview-sheet-enter-active,
.preview-sheet-leave-active {
  transition: opacity 0.22s ease, transform 0.22s ease;
}
.preview-sheet-enter-from,
.preview-sheet-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(20px);

  @media (min-width: 768px) {
    transform: translate(-50%, -45%);
  }
}

@media (prefers-reduced-motion: reduce) {
  .preview-fade-enter-active,
  .preview-fade-leave-active,
  .preview-sheet-enter-active,
  .preview-sheet-leave-active {
    transition-duration: 0.01s;
  }
}
</style>
