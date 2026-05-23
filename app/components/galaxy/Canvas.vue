<template>
  <div ref="wrapEl" class="galaxy-canvas-wrap">
    <canvas
      ref="canvasEl"
      :class="{ 'cursor-pointer': hoveredId != null }"
      role="img"
      tabindex="0"
      :aria-label="
        $t(
          'galaxy.canvasLabel',
          'Initiative ecosystem. Use arrow keys to move between initiatives, Enter to open.'
        )
      "
      :aria-activedescendant="focusedId != null ? `galaxy-node-${focusedId}` : undefined"
      @focus="onCanvasFocus"
      @blur="onCanvasBlur"
      @keydown="onCanvasKeydown"
    />
    <div class="galaxy-zoom-controls" aria-hidden="true">
      <button
        type="button"
        class="zoom-btn"
        :aria-label="$t('galaxy.zoomIn', 'Zoom in')"
        @click="zoomBy(1.4)"
      >
        <v-icon size="small">mdi-plus</v-icon>
      </button>
      <button
        type="button"
        class="zoom-btn"
        :aria-label="$t('galaxy.zoomOut', 'Zoom out')"
        @click="zoomBy(1 / 1.4)"
      >
        <v-icon size="small">mdi-minus</v-icon>
      </button>
      <button
        type="button"
        class="zoom-btn"
        :aria-label="$t('galaxy.resetZoom', 'Reset zoom')"
        @click="resetZoom"
      >
        <v-icon size="small">mdi-image-filter-center-focus</v-icon>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { quadtree, type Quadtree } from 'd3-quadtree'
import { select } from 'd3-selection'
import { zoom, zoomIdentity, type ZoomTransform, type D3ZoomEvent } from 'd3-zoom'

const props = defineProps<{
  nodes: GalaxyNode[]
  domain: { x: [number, number]; y: [number, number] }
  continentColors: Record<string, string>
  visibleIds?: Set<number> | null
}>()

const emit = defineEmits<{
  hover: [payload: { node: GalaxyNode; clientX: number; clientY: number } | null]
  select: [node: GalaxyNode]
}>()

const { t: $t } = useI18n()

const wrapEl = ref<HTMLDivElement | null>(null)
const canvasEl = ref<HTMLCanvasElement | null>(null)
const hoveredId = ref<number | null>(null)
const focusedId = ref<number | null>(null)

let width = 0
let height = 0
let dpr = 1
let ctx: CanvasRenderingContext2D | null = null
let raf: number | null = null
let resizeObserver: ResizeObserver | null = null

// Domain → fit transform (constant for a given canvas size; rebuilt on resize).
let fitScale = 1
let fitTx = 0
let fitTy = 0

// User pan/zoom transform (composed on top of fit transform).
let userTransform: ZoomTransform = zoomIdentity

let tree: Quadtree<GalaxyNode> | null = null

// Distinguishes click from drag.
let pressedAt: { x: number; y: number } | null = null
const TAP_DRAG_THRESHOLD = 8

const reducedMotion = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

const requestDraw = () => {
  if (raf == null && typeof window !== 'undefined') {
    raf = window.requestAnimationFrame(draw)
  }
}

// Convert a screen-space point (CSS pixels relative to the canvas) to data-space.
const screenToData = (sx: number, sy: number) => {
  // canvas → fit space: (s - canvasCenter) / fitScale + dataCenter
  // user transform applies on top
  const fx = userTransform.invertX(sx)
  const fy = userTransform.invertY(sy)
  const dx = (fx - width / 2) / fitScale + (props.domain.x[0] + props.domain.x[1]) / 2
  const dy = (fy - height / 2) / fitScale + (props.domain.y[0] + props.domain.y[1]) / 2
  return { x: dx, y: dy }
}

const computeFitTransform = () => {
  const dx = props.domain.x[1] - props.domain.x[0]
  const dy = props.domain.y[1] - props.domain.y[0]
  if (dx <= 0 || dy <= 0 || width <= 0 || height <= 0) {
    fitScale = 1
    fitTx = 0
    fitTy = 0
    return
  }
  const padding = 40
  fitScale = Math.min((width - padding * 2) / dx, (height - padding * 2) / dy)
  fitTx = width / 2 - ((props.domain.x[0] + props.domain.x[1]) / 2) * fitScale
  fitTy = height / 2 - ((props.domain.y[0] + props.domain.y[1]) / 2) * fitScale
}

const draw = () => {
  raf = null
  if (!ctx) return

  ctx.save()
  ctx.setTransform(dpr, 0, 0, dpr, 0, 0)
  ctx.clearRect(0, 0, width, height)

  // Apply user transform first (zoom/pan), then fit transform.
  ctx.translate(userTransform.x, userTransform.y)
  ctx.scale(userTransform.k, userTransform.k)
  ctx.translate(fitTx, fitTy)
  ctx.scale(fitScale, fitScale)

  const visible = props.visibleIds ?? null
  // Two-pass draw so dimmed nodes never paint over visible ones.
  if (visible) {
    ctx.globalAlpha = 0.15
    for (const node of props.nodes) {
      if (visible.has(node.id)) continue
      ctx.fillStyle = props.continentColors[node.continent] ?? '#888'
      ctx.beginPath()
      ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2)
      ctx.fill()
    }
    ctx.globalAlpha = 1
  }

  for (const node of props.nodes) {
    if (visible && !visible.has(node.id)) continue
    ctx.fillStyle = props.continentColors[node.continent] ?? '#888'
    ctx.beginPath()
    ctx.arc(node.x, node.y, node.r, 0, Math.PI * 2)
    ctx.fill()

    if (node.id === hoveredId.value || node.id === focusedId.value) {
      ctx.lineWidth = 2 / (userTransform.k * fitScale)
      ctx.strokeStyle = '#27421d'
      ctx.stroke()
    }

    // Persistent focus ring (keyboard nav) — drawn larger so it reads as focus
    if (node.id === focusedId.value) {
      ctx.lineWidth = 1.5 / (userTransform.k * fitScale)
      ctx.strokeStyle = '#27421d'
      ctx.beginPath()
      ctx.arc(node.x, node.y, node.r + 4 / (userTransform.k * fitScale), 0, Math.PI * 2)
      ctx.stroke()
    }
  }

  ctx.restore()
}

const buildTree = () => {
  tree = quadtree<GalaxyNode>()
    .x((n) => n.x)
    .y((n) => n.y)
    .addAll(props.nodes)
}

const findNodeAt = (clientX: number, clientY: number): GalaxyNode | undefined => {
  if (!tree || !canvasEl.value) return undefined
  const rect = canvasEl.value.getBoundingClientRect()
  const sx = clientX - rect.left
  const sy = clientY - rect.top
  const { x, y } = screenToData(sx, sy)
  // Tolerance grows with effective scale so users always have room to land on a dot.
  const effectiveScale = userTransform.k * fitScale
  const tolerance = Math.max(6, 10 / effectiveScale)
  const node = tree.find(x, y, tolerance)
  // Hit-testing respects the filter: dimmed nodes are not interactive.
  if (node && props.visibleIds && !props.visibleIds.has(node.id)) return undefined
  return node
}

const onPointerMove = (e: PointerEvent) => {
  const node = findNodeAt(e.clientX, e.clientY)
  const newId = node?.id ?? null
  if (newId !== hoveredId.value) {
    hoveredId.value = newId
    requestDraw()
    emit(
      'hover',
      node ? { node, clientX: e.clientX, clientY: e.clientY } : null
    )
  } else if (node) {
    // Same node, but cursor moved — keep tooltip glued.
    emit('hover', { node, clientX: e.clientX, clientY: e.clientY })
  }
}

const onPointerLeave = () => {
  if (hoveredId.value != null) {
    hoveredId.value = null
    requestDraw()
    emit('hover', null)
  }
}

const onPointerDown = (e: PointerEvent) => {
  pressedAt = { x: e.clientX, y: e.clientY }
}

const onPointerUp = (e: PointerEvent) => {
  if (!pressedAt) return
  const dragDist = Math.hypot(e.clientX - pressedAt.x, e.clientY - pressedAt.y)
  pressedAt = null
  if (dragDist > TAP_DRAG_THRESHOLD) return // it was a pan, not a tap
  const node = findNodeAt(e.clientX, e.clientY)
  if (node) emit('select', node)
}

let zoomBehavior: ReturnType<typeof zoom<HTMLCanvasElement, unknown>> | null = null

const setupZoom = () => {
  if (!canvasEl.value) return
  zoomBehavior = zoom<HTMLCanvasElement, unknown>()
    .scaleExtent([0.5, 8])
    .on('zoom', (e: D3ZoomEvent<HTMLCanvasElement, unknown>) => {
      userTransform = e.transform
      requestDraw()
    })
  select(canvasEl.value).call(zoomBehavior)
}

const zoomBy = (factor: number) => {
  if (!zoomBehavior || !canvasEl.value) return
  const sel = select(canvasEl.value)
  if (reducedMotion()) {
    zoomBehavior.scaleBy(sel, factor)
  } else {
    zoomBehavior.scaleBy(sel.transition().duration(200) as never, factor)
  }
}

const resetZoom = () => {
  if (!zoomBehavior || !canvasEl.value) return
  const sel = select(canvasEl.value)
  if (reducedMotion()) {
    zoomBehavior.transform(sel, zoomIdentity)
  } else {
    zoomBehavior.transform(sel.transition().duration(250) as never, zoomIdentity)
  }
}

// Keyboard navigation: focus a starting node on canvas focus, arrow keys
// move to nearest neighbor in direction, Enter selects.
const candidateNodes = (): GalaxyNode[] => {
  if (props.visibleIds) {
    return props.nodes.filter((n) => props.visibleIds!.has(n.id))
  }
  return props.nodes
}

const findNearestInDirection = (
  fromId: number,
  dx: number,
  dy: number
): GalaxyNode | null => {
  const candidates = candidateNodes()
  const from = candidates.find((n) => n.id === fromId)
  if (!from) return candidates[0] ?? null

  let best: GalaxyNode | null = null
  let bestScore = Infinity

  for (const node of candidates) {
    if (node.id === fromId) continue
    const ex = node.x - from.x
    const ey = node.y - from.y
    // Project onto desired direction; require positive projection.
    const projected = ex * dx + ey * dy
    if (projected <= 0) continue
    // Penalise off-axis distance more than along-axis distance (cone-shaped).
    const orthogonal = Math.abs(ex * -dy + ey * dx)
    const score = orthogonal * 2 - projected * 0.5 + Math.hypot(ex, ey) * 0.1
    if (score < bestScore) {
      bestScore = score
      best = node
    }
  }
  return best
}

// Keep the focused node in view by gently centring on it.
const centerOnNode = (node: GalaxyNode) => {
  if (!zoomBehavior || !canvasEl.value) return
  // The current effective transform maps data → screen as:
  //   screenX = userTransform.x + userTransform.k * (fitTx + fitScale * dataX)
  // We want the node at canvas center: screenX = width / 2 ⇒ solve for
  // userTransform.x. Same for y.
  const targetK = userTransform.k
  const tx = width / 2 - targetK * (fitTx + fitScale * node.x)
  const ty = height / 2 - targetK * (fitTy + fitScale * node.y)
  const next = zoomIdentity.translate(tx, ty).scale(targetK)
  const sel = select(canvasEl.value)
  if (reducedMotion()) {
    zoomBehavior.transform(sel, next)
  } else {
    zoomBehavior.transform(sel.transition().duration(180) as never, next)
  }
}

const onCanvasFocus = () => {
  if (focusedId.value != null) return
  const candidates = candidateNodes()
  if (candidates.length > 0) {
    focusedId.value = candidates[0].id
    requestDraw()
  }
}

const onCanvasBlur = () => {
  focusedId.value = null
  requestDraw()
}

const onCanvasKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    focusedId.value = null
    requestDraw()
    canvasEl.value?.blur()
    return
  }

  if (e.key === 'Enter' || e.key === ' ') {
    if (focusedId.value != null) {
      const node = props.nodes.find((n) => n.id === focusedId.value)
      if (node) {
        e.preventDefault()
        emit('select', node)
      }
    }
    return
  }

  let dx = 0
  let dy = 0
  if (e.key === 'ArrowRight') dx = 1
  else if (e.key === 'ArrowLeft') dx = -1
  else if (e.key === 'ArrowDown') dy = 1
  else if (e.key === 'ArrowUp') dy = -1
  else return

  e.preventDefault()
  if (focusedId.value == null) {
    const candidates = candidateNodes()
    if (candidates.length > 0) focusedId.value = candidates[0].id
  } else {
    const next = findNearestInDirection(focusedId.value, dx, dy)
    if (next) {
      focusedId.value = next.id
      centerOnNode(next)
    }
  }
  requestDraw()
}

const resize = () => {
  if (!wrapEl.value || !canvasEl.value) return
  const rect = wrapEl.value.getBoundingClientRect()
  width = rect.width
  height = rect.height
  dpr = window.devicePixelRatio || 1
  canvasEl.value.width = Math.max(1, Math.floor(width * dpr))
  canvasEl.value.height = Math.max(1, Math.floor(height * dpr))
  canvasEl.value.style.width = `${width}px`
  canvasEl.value.style.height = `${height}px`
  ctx = canvasEl.value.getContext('2d')
  computeFitTransform()
  requestDraw()
}

onMounted(() => {
  if (typeof window === 'undefined') return
  resize()
  buildTree()
  setupZoom()

  resizeObserver = new ResizeObserver(resize)
  resizeObserver.observe(wrapEl.value!)

  const c = canvasEl.value!
  c.addEventListener('pointermove', onPointerMove)
  c.addEventListener('pointerleave', onPointerLeave)
  c.addEventListener('pointerdown', onPointerDown)
  c.addEventListener('pointerup', onPointerUp)
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  resizeObserver = null
  if (raf != null) {
    cancelAnimationFrame(raf)
    raf = null
  }
  const c = canvasEl.value
  if (c) {
    c.removeEventListener('pointermove', onPointerMove)
    c.removeEventListener('pointerleave', onPointerLeave)
    c.removeEventListener('pointerdown', onPointerDown)
    c.removeEventListener('pointerup', onPointerUp)
  }
})

// Rebuild quadtree when node set changes (e.g., filter introduces new ids).
watch(
  () => props.nodes,
  () => {
    buildTree()
    requestDraw()
  },
  { deep: false }
)

// Visible-id changes don't move nodes — just opacity. Single redraw, no rebuild.
watch(() => props.visibleIds, requestDraw)

watch(
  () => props.domain,
  () => {
    computeFitTransform()
    requestDraw()
  },
  { deep: true }
)
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.galaxy-canvas-wrap {
  position: relative;
  width: 100%;
  height: 100%;
  background: $galaxy-canvas-bg;
}

canvas {
  display: block;
  touch-action: none; // d3-zoom handles all pointer events
  cursor: grab;

  &:active {
    cursor: grabbing;
  }

  &.cursor-pointer {
    cursor: pointer;
  }

  &:focus {
    outline: none;
  }

  &:focus-visible {
    outline: 3px solid $green-dark;
    outline-offset: -3px;
  }
}

.galaxy-zoom-controls {
  position: absolute;
  right: $spacing-sm;
  bottom: $spacing-sm;
  display: flex;
  flex-direction: column;
  gap: 4px;
  z-index: 2;

  .zoom-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 6px;
    background: $galaxy-legend-bg;
    border: 1px solid rgba(0, 0, 0, 0.08);
    color: rgba(0, 0, 0, 0.65);
    cursor: pointer;
    transition: background 0.15s, color 0.15s;

    &:hover {
      background: white;
      color: $green-dark;
    }

    &:focus-visible {
      outline: 2px solid $green-dark;
      outline-offset: 2px;
    }
  }
}
</style>
