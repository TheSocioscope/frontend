<template>
  <section class="map-section">
    <div class="container">
      <div class="section-header section-reveal">
        <h2>{{ $t('map.title') }}</h2>
      </div>

      <div ref="mapContainer" class="map-container section-reveal">
        <svg ref="svgMap" class="world-map" />
        <div v-if="selectedLocation" class="map-tooltip" :style="tooltipStyle">
          <div class="tooltip-country">{{ selectedLocation.name }}</div>
          <div class="tooltip-cases">{{ selectedLocation.cases }}</div>
          <div class="tooltip-label">{{ $t('map.projects', 'projects') }}</div>
          <div class="tooltip-action">{{ $t('map.clickToView', 'Click to view projects') }}</div>
        </div>

        <!-- Zoom controls — mobile only. On desktop the map is fixed
             (no pinch / scroll / pan zoom), so these aren't shown. -->
        <div v-if="dataLoaded && !isDesktop" class="map-controls">
          <button
            type="button"
            class="map-btn"
            :aria-label="$t('map.zoomIn', 'Zoom in')"
            @click="zoomBy(1.5)"
          >
            <v-icon size="small">mdi-plus</v-icon>
          </button>
          <button
            type="button"
            class="map-btn"
            :aria-label="$t('map.zoomOut', 'Zoom out')"
            @click="zoomBy(1 / 1.5)"
          >
            <v-icon size="small">mdi-minus</v-icon>
          </button>
          <button
            type="button"
            class="map-btn"
            :aria-label="$t('map.resetZoom', 'Reset zoom')"
            @click="resetZoom"
          >
            <v-icon size="small">mdi-image-filter-center-focus</v-icon>
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { feature } from 'topojson-client'

interface LocationData {
  name: string
  lat: number
  lon: number
  cases: number
  countryCode: string
}

interface CountryStats {
  [countryCode: string]: {
    count: number
    projects: Array<{
      pubId: number
      name: string
    }>
  }
}

const { t: $t } = useI18n()
const router = useRouter()
const localePath = useLocalePath()
const config = useRuntimeConfig()
const { countryCodeToMapName, getCountryCode } = useCountryMapping()
const mapContainer = ref<HTMLElement | null>(null)
const svgMap = ref<SVGElement | null>(null)
const selectedLocation = ref<LocationData | null>(null)
const tooltipStyle = ref<Record<string, string>>({})

// Load country stats from generated JSON
const countryStats = ref<CountryStats>({})
const countryData = ref<Record<string, number>>({})
const dataLoaded = ref(false)
// Desktop gets a fixed map (no zoom/pan, no zoom buttons); phones keep it.
const isDesktop = ref(true)

onMounted(async () => {
  isDesktop.value = typeof window !== 'undefined' && window.innerWidth > 600
  try {
    const baseURL = config.app.baseURL || '/'
    const response = await fetch(`${baseURL}data/country-stats.json`)
    countryStats.value = await response.json()

    // Convert country codes to map names with counts
    for (const [code, stats] of Object.entries(countryStats.value)) {
      const mapName = countryCodeToMapName[code]
      if (mapName) {
        countryData.value[mapName] = stats.count
      } else {
        console.warn(`No mapping found for country code: ${code}`)
      }
    }

    dataLoaded.value = true
  } catch (error) {
    console.error('Error loading country stats:', error)
  }
})

function getColor(cases: number | undefined): string {
  if (!cases) return '#f0f0f0'
  if (cases > 100) return '#1B5E20'
  if (cases > 50) return '#2E7D32'
  if (cases > 30) return '#388E3C'
  if (cases > 15) return '#4CAF50'
  if (cases > 5) return '#66BB6A'
  return '#81C784'
}

function handleCountryClick(countryName: string) {
  const countryCode = getCountryCode(countryName)
  if (countryCode && countryData.value[countryName]) {
    // Navigate to projects page with country filter
    router.push({
      path: localePath('/projects'),
      query: { countries: countryCode }
    })
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let svg: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let zoomGroup: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let zoomBehavior: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let projection: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let path: any

const reducedMotion = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

// Stepped color buckets — country fill scales with project count.
const COLOR_STEPS = [
  { threshold: 1, color: '#81C784', label: '1–5' },
  { threshold: 6, color: '#66BB6A', label: '6–15' },
  { threshold: 16, color: '#4CAF50', label: '16–30' },
  { threshold: 31, color: '#388E3C', label: '31–50' },
  { threshold: 51, color: '#2E7D32', label: '51–100' },
  { threshold: 101, color: '#1B5E20', label: '100+' }
]

const zoomBy = (factor: number) => {
  if (!svg || !zoomBehavior) return
  if (reducedMotion()) {
    zoomBehavior.scaleBy(svg, factor)
  } else {
    zoomBehavior.scaleBy(svg.transition().duration(220), factor)
  }
}

const resetZoom = () => {
  if (!svg || !zoomBehavior) return
  if (reducedMotion()) {
    zoomBehavior.transform(svg, d3.zoomIdentity)
  } else {
    zoomBehavior.transform(svg.transition().duration(280), d3.zoomIdentity)
  }
}

// Render map after data is loaded
watch(
  dataLoaded,
  async (loaded) => {
    if (!loaded || !svgMap.value || !mapContainer.value) {
      console.log('Map render conditions:', {
        loaded,
        svgMap: !!svgMap.value,
        mapContainer: !!mapContainer.value
      })
      return
    }

    console.log('Starting map render with', Object.keys(countryData.value).length, 'countries')

    // Set up SVG dimensions — responsive height so the map fills the
    // container without enormous vertical whitespace on mobile.
    const width = mapContainer.value.clientWidth
    const height = Math.min(560, Math.max(220, Math.round(width * 0.55)))

    svg = d3.select(svgMap.value)
    svg.selectAll('*').remove() // Clear any existing content
    svg
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .style('width', '100%')
      .style('height', `${height}px`)

    // Natural-earth projection sized to fit the responsive viewBox.
    projection = d3
      .geoNaturalEarth1()
      .scale(Math.min(width / 6, height / 2.6))
      .translate([width / 2, height / 1.9])

    path = d3.geoPath().projection(projection)

    // Load and render world map
    try {
      const worldData = await fetch(
        'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json'
      ).then((response) => response.json())

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const countries: any = feature(worldData, worldData.objects.countries)

      // All paths live inside a zoom group so d3-zoom transforms the
      // whole geography (not just the SVG element).
      zoomGroup = svg.append('g').attr('class', 'map-zoom')

      zoomGroup
        .selectAll('path')
        .data(countries.features)
        .join('path')
        .attr('class', 'country')
        .attr('d', path)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('fill', (d: any) => {
          const countryName = d.properties.name
          const cases = countryData.value[countryName]
          return getColor(cases)
        })
        .attr('stroke', '#fff')
        .attr('stroke-width', 0.5)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .style('cursor', (d: any) => (countryData.value[d.properties.name] ? 'pointer' : 'default'))
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .on('mouseover', function (this: any, event: MouseEvent, d: any) {
          const countryName = d.properties.name
          const cases = countryData.value[countryName]

          if (cases) {
            d3.select(this).attr('stroke', '#2E7D32').attr('stroke-width', 2)

            const countryCode = getCountryCode(countryName)
            selectedLocation.value = {
              name: countryName,
              cases,
              lat: 0,
              lon: 0,
              countryCode: countryCode || ''
            }
            updateTooltipPosition(event)
          }
        })
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .on('mouseout', function (this: any) {
          d3.select(this).attr('stroke', '#fff').attr('stroke-width', 0.5)

          selectedLocation.value = null
        })
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .on('click', function (this: any, event: MouseEvent, d: any) {
          const countryName = d.properties.name
          if (countryData.value[countryName]) {
            handleCountryClick(countryName)
          }
        })

      console.log('Map rendered successfully')

      // Zoom/pan — phones only. On desktop the map stays fixed at the
      // world-fit view, so we don't wire up d3-zoom at all (no wheel/pinch
      // capture, no drag-to-pan, no zoom buttons).
      if (!isDesktop.value) {
        // scaleExtent caps how far in/out the user can go (1× = world fit,
        // 8× = country detail).
        zoomBehavior = d3
          .zoom()
          .scaleExtent([1, 8])
          // eslint-disable-next-line @typescript-eslint/no-explicit-any
          .on('zoom', (event: any) => {
            zoomGroup.attr('transform', event.transform.toString())
            // Counter-scale strokes so country borders don't fatten as
            // you zoom in.
            zoomGroup.selectAll('path.country').attr('stroke-width', 0.5 / event.transform.k)
          })

        svg.call(zoomBehavior)
      }
    } catch (error) {
      console.error('Error loading map data:', error)
    }
  },
  { immediate: true }
)

function updateTooltipPosition(event: MouseEvent) {
  if (!mapContainer.value) return

  const rect = mapContainer.value.getBoundingClientRect()
  tooltipStyle.value = {
    left: `${event.clientX - rect.left + 10}px`,
    top: `${event.clientY - rect.top - 50}px`
  }
}

// Handle window resize
onMounted(() => {
  const handleResize = () => {
    if (!svgMap.value || !mapContainer.value) return
    // In production, you'd want to redraw the map on resize
  }

  window.addEventListener('resize', handleResize)

  onBeforeUnmount(() => {
    window.removeEventListener('resize', handleResize)
  })
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.map-section {
  background: $warm-beige;
  padding: 3.5rem 0;

  @media (max-width: 768px) {
    padding: 2rem 0;
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;

  @media (max-width: 768px) {
    padding: 0 1rem;
  }
}

.map-container {
  position: relative;
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  /* overflow: hidden so panned/zoomed countries don't leak past the
     rounded corners. */
  overflow: hidden;
  padding: 20px;

  @media (max-width: 768px) {
    padding: 12px;
    border-radius: 8px;
  }
}

/* Zoom controls — bottom-left desktop, bottom-right mobile (mirror of
   the projects map placement so users see consistent UX). */
.map-controls {
  position: absolute;
  left: 12px;
  bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 2;

  @media (max-width: 600px) {
    left: auto;
    right: 8px;
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
  transition:
    background 0.15s,
    color 0.15s,
    border-color 0.15s;

  &:hover {
    background: white;
    color: $green-dark;
    border-color: $green-bright;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
    z-index: 1;
  }

  &:active {
    background: $earth-10;
  }

  @media (max-width: 600px) {
    width: 32px;
    height: 32px;
  }
}

/* Tighten the section heading on mobile too — currently it shows
   "Map of case studies" at huge serif size with margin gaps below */
.section-header {
  margin-bottom: 1.25rem;

  h2 {
    font-family: $font-family-display;
    font-size: 2rem;
    font-weight: $font-weight-bold;
    color: $brown-dark;
    line-height: 1.15;
    margin: 0;

    @media (max-width: 768px) {
      font-size: 1.5rem;
    }
  }
}

.world-map {
  display: block;
  width: 100%;
  height: auto;
}

.map-tooltip {
  position: absolute;
  padding: 12px 16px;
  background: white;
  border: 2px solid #2e7d32;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  pointer-events: none;
  z-index: 1000;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 14px;

  &:has(.tooltip-country) {
    opacity: 1;
  }

  .tooltip-country {
    font-weight: 600;
    color: #2c2416;
    margin-bottom: 4px;
  }

  .tooltip-cases {
    color: #2e7d32;
    font-size: 20px;
    font-weight: bold;
  }

  .tooltip-label {
    color: #8b6f47;
    font-size: 12px;
  }

  .tooltip-action {
    color: #2e7d32;
    font-size: 11px;
    margin-top: 4px;
    font-style: italic;
  }
}

:deep(.data-points) {
  circle {
    transition: all 0.2s ease;
  }
}
</style>
