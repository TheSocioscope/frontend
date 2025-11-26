<template>
  <section class="section map-section">
    <v-container>
      <h2 class="map-title text-center">
        {{ $t('map.title') }}
      </h2>
      <p class="map-subtitle text-center">
        {{ $t('map.subtitle') }}
      </p>

      <div ref="mapContainer" class="map-container">
        <svg ref="svgMap" class="world-map" />
        <div v-if="selectedLocation" class="map-tooltip" :style="tooltipStyle">
          <div class="tooltip-country">{{ selectedLocation.name }}</div>
          <div class="tooltip-cases">{{ selectedLocation.cases }}</div>
          <div class="tooltip-label">documented cases</div>
        </div>
      </div>
    </v-container>
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
}

const { t: $t } = useI18n()
const mapContainer = ref<HTMLElement | null>(null)
const svgMap = ref<SVGElement | null>(null)
const selectedLocation = ref<LocationData | null>(null)
const tooltipStyle = ref<Record<string, string>>({})

// Country data with case counts from the original HTML
const countryData: Record<string, number> = {
  Argentina: 59,
  Armenia: 3,
  Canada: 2,
  Colombia: 159,
  'Costa Rica': 29,
  Denmark: 42,
  Ecuador: 28,
  France: 79,
  Georgia: 2,
  'United Kingdom': 16,
  India: 7,
  Japan: 2,
  Kenya: 50,
  Lithuania: 2,
  Mexico: 10,
  Morocco: 14,
  'New Zealand': 1,
  Paraguay: 6,
  Peru: 39,
  Philippines: 1,
  Poland: 5,
  Rwanda: 3,
  'South Africa': 11,
  Spain: 36,
  'Sri Lanka': 4,
  Switzerland: 4,
  Tanzania: 2,
  Uganda: 3,
  'United States': 7,
  'Hong Kong': 1
}

function getColor(cases: number | undefined): string {
  if (!cases) return '#f0f0f0'
  if (cases > 100) return '#1B5E20'
  if (cases > 50) return '#2E7D32'
  if (cases > 30) return '#388E3C'
  if (cases > 15) return '#4CAF50'
  if (cases > 5) return '#66BB6A'
  return '#81C784'
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
let svg: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let projection: any
// eslint-disable-next-line @typescript-eslint/no-explicit-any
let path: any

onMounted(async () => {
  if (!svgMap.value || !mapContainer.value) return

  // Set up SVG dimensions
  const width = mapContainer.value.clientWidth
  const height = 600

  svg = d3.select(svgMap.value).attr('width', width).attr('height', height)

  // Set up projection - using geoNaturalEarth1 like the original
  projection = d3
    .geoNaturalEarth1()
    .scale(width / 6.5)
    .translate([width / 2, height / 2])

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
        const cases = countryData[countryName]
        return getColor(cases)
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 0.5)
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .style('cursor', (d: any) => (countryData[d.properties.name] ? 'pointer' : 'default'))
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('mouseover', function (this: any, event: MouseEvent, d: any) {
        const countryName = d.properties.name
        const cases = countryData[countryName]

        if (cases) {
          d3.select(this).attr('stroke', '#2E7D32').attr('stroke-width', 2)

          selectedLocation.value = { name: countryName, cases, lat: 0, lon: 0 }
          updateTooltipPosition(event)
        }
      })
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('mouseout', function (this: any) {
        d3.select(this).attr('stroke', '#fff').attr('stroke-width', 0.5)

        selectedLocation.value = null
      })

    // Add zoom behavior
    const zoom = d3
      .zoom()
      .scaleExtent([1, 8])
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('zoom', (event: any) => {
        svg.selectAll('g').attr('transform', event.transform)
      })

    svg.call(zoom)
  } catch (error) {
    console.error('Error loading map data:', error)
  }
})

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
@use '../../assets/styles/variables' as *;

.map-section {
  background: linear-gradient(135deg, $surface-cream 0%, $cream-light 100%);
  padding: $spacing-4xl 0;
}

.map-description {
  font-size: 1.3rem;
  color: $brown-dark;
  max-width: 800px;
  margin: 0 auto $spacing-3xl;
  line-height: 1.7;

  @media (max-width: 768px) {
    font-size: 1.1rem;
  }
}

.map-container {
  position: relative;
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
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
}

:deep(.data-points) {
  circle {
    transition: all 0.2s ease;
  }
}
</style>
