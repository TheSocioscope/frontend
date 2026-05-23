<template>
  <Transition name="galaxy-tooltip">
    <div
      v-if="payload"
      class="galaxy-tooltip"
      :style="{ transform: `translate3d(${x}px, ${y}px, 0)` }"
      role="tooltip"
    >
      <div class="tooltip-row tooltip-name">
        <span class="dot" :style="{ background: continentColors[payload.node.continent] || '#888' }" />
        <span>{{ payload.node.slug }}</span>
      </div>
      <div class="tooltip-row tooltip-meta">
        <span class="meta-label">{{ $t('galaxy.sectorLabel', 'Sector') }}:</span>
        <span>{{ payload.node.sector }}</span>
      </div>
      <div class="tooltip-row tooltip-meta">
        <span class="meta-label">{{ $t('galaxy.continentLabel', 'Continent') }}:</span>
        <span>{{ payload.node.continent }}</span>
      </div>
    </div>
  </Transition>
</template>

<script setup lang="ts">
const props = defineProps<{
  payload: { node: GalaxyNode; clientX: number; clientY: number } | null
  continentColors: Record<string, string>
  parentRect: DOMRect | null
}>()

const { t: $t } = useI18n()

// Position relative to the galaxy parent (not viewport) so it scrolls with the page.
// Offset 12/16 from cursor; flip to the left edge if the tooltip would overflow.
const TOOLTIP_W = 240
const TOOLTIP_H = 96
const x = computed(() => {
  if (!props.payload || !props.parentRect) return 0
  const local = props.payload.clientX - props.parentRect.left
  const wouldOverflow = local + 12 + TOOLTIP_W > props.parentRect.width
  return wouldOverflow ? local - TOOLTIP_W - 12 : local + 12
})
const y = computed(() => {
  if (!props.payload || !props.parentRect) return 0
  const local = props.payload.clientY - props.parentRect.top
  const wouldOverflow = local + 16 + TOOLTIP_H > props.parentRect.height
  return wouldOverflow ? local - TOOLTIP_H - 16 : local + 16
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.galaxy-tooltip {
  position: absolute;
  top: 0;
  left: 0;
  width: 240px;
  background: $galaxy-tooltip-bg;
  border-radius: $galaxy-tooltip-radius;
  box-shadow: $galaxy-tooltip-shadow;
  padding: $spacing-sm;
  pointer-events: none;
  z-index: 5;
  font-size: 0.875rem;
  color: rgba(0, 0, 0, 0.87);
}

.tooltip-row {
  display: flex;
  align-items: center;
  gap: $spacing-xs;

  & + & {
    margin-top: 4px;
  }
}

.tooltip-name {
  font-weight: 600;
  color: $green-dark;
  margin-bottom: 4px;
}

.tooltip-meta {
  font-size: 0.8125rem;
  color: rgba(0, 0, 0, 0.6);

  .meta-label {
    color: rgba(0, 0, 0, 0.45);
    text-transform: uppercase;
    font-size: 0.6875rem;
    letter-spacing: 0.04em;
  }
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

// Fade in/out (skipped under reduced-motion via the global media query)
.galaxy-tooltip-enter-active,
.galaxy-tooltip-leave-active {
  transition: opacity 0.12s ease;
}

.galaxy-tooltip-enter-from,
.galaxy-tooltip-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .galaxy-tooltip-enter-active,
  .galaxy-tooltip-leave-active {
    transition: none;
  }
}
</style>
