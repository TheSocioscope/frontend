<template>
  <section class="map-section">
    <div class="container">
      <div class="section-header">
        <h2>{{ $t('map.title') }}</h2>
      </div>

      <div ref="mapContainer" class="map-container">
        <svg ref="svgMap" class="world-map" />
        <div v-if="selectedLocation" class="map-tooltip" :style="tooltipStyle">
          <div class="tooltip-country">{{ selectedLocation.name }}</div>
          <div class="tooltip-cases">{{ selectedLocation.cases }}</div>
          <div class="tooltip-label">{{ $t('map.projects', 'projects') }}</div>
          <div class="tooltip-action">{{ $t('map.clickToView', 'Click to view projects') }}</div>
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

onMounted(async () => {
  try {
    const baseURL = config.app.baseURL || '/'
    const response = await fetch(`${baseURL}data/country-stats.json`)
    countryStats.value = await response.json()

    console.log('Loaded country stats:', Object.keys(countryStats.value).length, 'countries')

    // Convert country codes to map names with counts
    for (const [code, stats] of Object.entries(countryStats.value)) {
      const mapName = countryCodeToMapName[code]
      if (mapName) {
        countryData.value[mapName] = stats.count
        console.log(`Mapped: ${code} -> ${mapName} (${stats.count} projects)`)
      } else {
        console.warn(`No mapping found for country code: ${code}`)
      }
    }

    console.log('Country data for map:', Object.keys(countryData.value).length, 'countries')
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
      path: '/projects',
      query: { countries: countryCode }
    })
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let svg: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let projection: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let path: any

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

    // Set up SVG dimensions
    const width = mapContainer.value.clientWidth
    const height = 600

    svg = d3.select(svgMap.value)
    svg.selectAll('*').remove() // Clear any existing content
    svg
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('preserveAspectRatio', 'xMidYMid meet')
      .style('width', '100%')
      .style('height', 'auto')

    // Set up projection - using geoNaturalEarth1 with adjusted scale and translation to fit within viewBox
    projection = d3
      .geoNaturalEarth1()
      .scale(width / 7)
      .translate([width / 2, height / 1.8])

    path = d3.geoPath().projection(projection)

    // Load and render world map
    try {
      const worldData = await fetch(
        'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json'
      ).then((response) => response.json())

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      const countries: any = feature(worldData, worldData.objects.countries)

      // Draw countries with fill based on case count
      svg
        .append('g')
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

      /*  // Add zoom behavior
    const zoom = d3
      .zoom()
      .scaleExtent([1, 8])
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('zoom', (event: any) => {
        svg.selectAll('g').attr('transform', event.transform)
      })

    svg.call(zoom)*/
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
  padding: 6rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.map-container {
  position: relative;
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: visible;
  padding: 20px;
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
