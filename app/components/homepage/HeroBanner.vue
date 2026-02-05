<template>
  <section ref="heroRef" class="hero" @mousemove="handleMouseMove" @mouseleave="handleMouseLeave">
    <canvas id="canvas" />
    <!-- Animated Circles Background -->
    <div class="hero-circles">
      <div class="circle-wrapper" :style="circle1Style">
        <div class="radial-glow" />
        <div class="circle circle-1" />
      </div>
      <div class="circle-wrapper" :style="circle2Style">
        <div class="circle circle-2" />
      </div>
      <div class="circle-wrapper" :style="circle3Style">
        <div class="circle circle-3" />
      </div>
    </div>

    <!-- Hero Content -->
    <div class="container">
      <div class="hero-content">
        <h1 class="hero-title">{{ $t('hero.title') }}</h1>
        <p class="hero-subtitle">{{ $t('hero.subtitle') }}</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

// Mouse tracking for circles
const heroRef = ref<HTMLElement | null>(null)
const mouseX = ref(0)
const mouseY = ref(0)
let idleTimeout: ReturnType<typeof setTimeout> | null = null

// Helper to calculate circle style based on size multiplier
// sizeMultiplier: bigger value = bigger circle
// Bigger circles get bigger offset, smaller circles get bigger scale reduction
const getCircleOffset = (sizeMultiplier: number) => {
  // Calculate distance from center using Pythagorean theorem
  const distance = Math.sqrt(mouseX.value ** 2 + mouseY.value ** 2)
  const maxDistance = 400 // Normalize distance

  // Offset: bigger circles move more (proportional to size)
  const maxOffset = 40 * sizeMultiplier
  const offsetX = -(mouseX.value / 8) * sizeMultiplier
  const offsetY = -(mouseY.value / 8) * sizeMultiplier
  const clampedX = Math.max(-maxOffset, Math.min(maxOffset, offsetX))
  const clampedY = Math.max(-maxOffset, Math.min(maxOffset, offsetY))

  // Scale: smaller circles shrink more (inverse proportion to size)
  // Further from center = smaller scale
  const scaleReduction = (distance / maxDistance) * 0.4 * (1.5 - sizeMultiplier)
  const scale = Math.max(0.6, 1 - scaleReduction)

  return { transform: `translate(${clampedX}px, ${clampedY}px) scale(${scale})` }
}

// Computed styles for each circle - reactive to mouse position
// Size multipliers: 0.5 (smallest), 0.75 (medium), 1 (largest)
const circle1Style = computed(() => getCircleOffset(0.5))
const circle2Style = computed(() => getCircleOffset(0.75))
const circle3Style = computed(() => getCircleOffset(1))

const resetToIdle = () => {
  mouseX.value = 0
  mouseY.value = 0
}

const handleMouseMove = (event: MouseEvent) => {
  if (!heroRef.value) return

  // Clear existing idle timeout
  if (idleTimeout) {
    clearTimeout(idleTimeout)
  }

  const rect = heroRef.value.getBoundingClientRect()
  const centerX = rect.width / 2
  const centerY = rect.height / 2

  // Calculate position relative to center
  mouseX.value = event.clientX - rect.left - centerX
  mouseY.value = event.clientY - rect.top - centerY

  // Reset to idle after 3 seconds of no movement
  idleTimeout = setTimeout(resetToIdle, 3000)
}

const handleMouseLeave = () => {
  if (idleTimeout) {
    clearTimeout(idleTimeout)
  }
  mouseX.value = 0
  mouseY.value = 0
}

// Grass Animation
// Single rAF loop: growth + wind run simultaneously from frame 1.
// Positions are recomputed each frame into pre-allocated Float64Arrays,
// then drawn in two batched passes (compute → draw-by-segment-level)
// so that stroke() is called ~40 times per frame instead of 8 000.

interface GrassBlade {
  x: number
  y: number
  cumulativeAngles: number[] // absolute angle at each segment (encodes base + curve)
  segmentLength: number
  visibleSegments: number // grows 0 → SEGMENTS_PER_BLADE during the growth phase
  color: string
  phase: number // per-blade wind-sine phase offset
}

class GrassAnimation {
  private canvas: HTMLCanvasElement | null = null
  private context: CanvasRenderingContext2D | null = null
  private canvasWidth = 0
  private canvasHeight = 0
  private dpi = 1
  private blades: GrassBlade[] = []
  private animationFrame: number | null = null
  private startTime = 0
  private lastGrowTime = 0

  // Pre-allocated position buffers — reused every frame, zero per-frame allocation.
  // Layout per blade: [baseX, seg0X, seg1X … seg9X]  (stride = SEGMENTS_PER_BLADE + 1)
  private posX = new Float64Array(0)
  private posY = new Float64Array(0)

  private readonly MAX_BLADES = 800
  private readonly SEGMENTS_PER_BLADE = 10
  private readonly STRIDE = 11 // SEGMENTS_PER_BLADE + 1
  private readonly GROW_INTERVAL = 150 // ms between growth ticks
  private readonly BLADES_PER_TICK = 12
  private readonly WIND_STRENGTH = 0.3 // max tip sway in radians (~17°)
  private readonly WIND_SPEED = 0.002 // rad/ms  →  ~3 s full sway cycle
  private readonly WIND_RAMP = 2000 // ms to ramp wind from 0 → full

  // ── init ──────────────────────────────────────────────────────────────

  initialize(): void {
    this.canvas = document.getElementById('canvas') as HTMLCanvasElement
    if (!this.canvas) return

    const heroSection = this.canvas.parentElement
    if (!heroSection) return

    this.context = this.canvas.getContext('2d')
    if (!this.context) return

    this.dpi = window.devicePixelRatio || 1
    this.canvasWidth = heroSection.clientWidth
    this.canvasHeight = heroSection.clientHeight

    this.canvas.width = this.canvasWidth * this.dpi
    this.canvas.height = this.canvasHeight * this.dpi
    this.canvas.style.width = `${this.canvasWidth}px`
    this.canvas.style.height = `${this.canvasHeight}px`

    this.context.scale(this.dpi, this.dpi)
    this.context.lineCap = 'round' // sticky — set once, never changed

    this.posX = new Float64Array(this.MAX_BLADES * this.STRIDE)
    this.posY = new Float64Array(this.MAX_BLADES * this.STRIDE)

    this.startTime = performance.now()
    this.lastGrowTime = this.startTime - this.GROW_INTERVAL // first grow fires on frame 1
    this.animationFrame = requestAnimationFrame((time: number) => this.loop(time))
  }

  // ── main loop ─────────────────────────────────────────────────────────

  private loop(time: number): void {
    if (time - this.lastGrowTime >= this.GROW_INTERVAL) {
      this.growBlades()
      this.lastGrowTime = time
    }
    this.render(time)
    this.animationFrame = requestAnimationFrame((t: number) => this.loop(t))
  }

  // ── growth ────────────────────────────────────────────────────────────

  private growBlades(): void {
    for (const blade of this.blades) {
      if (blade.visibleSegments < this.SEGMENTS_PER_BLADE) blade.visibleSegments++
    }
    for (let i = 0; i < this.BLADES_PER_TICK && this.blades.length < this.MAX_BLADES; i++) {
      this.blades.push(this.createBlade())
    }
    // Sort by color so the draw loop can batch same-color segments
    // into single stroke() calls without extra bookkeeping.
    this.blades.sort((a, b) => (a.color < b.color ? -1 : a.color > b.color ? 1 : 0))
  }

  private createBlade(): GrassBlade {
    const x = Math.random() * this.canvasWidth
    const y = this.canvasHeight + 5
    const baseAngle = -Math.PI / 2 + (Math.random() - 0.5) * (Math.PI / 8)

    // Gaussian height via Box-Muller — mean 50 px, clamped 25–150 px
    const height = Math.max(25, Math.min(150, 50 + this.gaussianRandom() * 25))

    let color: string
    if (Math.random() < 0.5) {
      color = '#4ca049'
    } else {
      const others = ['#4caf50', '#6b8e23', '#8fbc8f']
      color = others[Math.floor(Math.random() * others.length)]
    }

    const segmentLength = height / this.SEGMENTS_PER_BLADE
    const cumulativeAngles = new Array<number>(this.SEGMENTS_PER_BLADE)
    let currentAngle = baseAngle

    for (let i = 0; i < this.SEGMENTS_PER_BLADE; i++) {
      currentAngle += (Math.random() - 0.5) * 0.1
      cumulativeAngles[i] = currentAngle
    }

    return {
      x,
      y,
      cumulativeAngles,
      segmentLength,
      visibleSegments: 0,
      color,
      phase: Math.random() * Math.PI * 2
    }
  }

  private gaussianRandom(): number {
    const u1 = Math.random()
    const u2 = Math.random()
    return Math.sqrt(-2 * Math.log(u1)) * Math.cos(2 * Math.PI * u2)
  }

  // ── render ────────────────────────────────────────────────────────────

  private render(time: number): void {
    if (!this.context || this.blades.length === 0) return
    const ctx = this.context

    ctx.clearRect(0, 0, this.canvasWidth, this.canvasHeight)

    const windRamp = Math.min(1, (time - this.startTime) / this.WIND_RAMP)

    // Pass 1 — compute every visible segment endpoint into the flat buffers.
    for (let b = 0; b < this.blades.length; b++) {
      const blade = this.blades[b]
      const base = b * this.STRIDE

      this.posX[base] = blade.x
      this.posY[base] = blade.y

      let cx = blade.x
      let cy = blade.y

      for (let i = 0; i < blade.visibleSegments; i++) {
        const progress = (i + 1) / this.SEGMENTS_PER_BLADE
        const windAngle =
          this.WIND_STRENGTH * progress * windRamp * Math.sin(time * this.WIND_SPEED + blade.phase)
        const angle = blade.cumulativeAngles[i] + windAngle

        cx += Math.cos(angle) * blade.segmentLength
        cy += Math.sin(angle) * blade.segmentLength
        this.posX[base + i + 1] = cx
        this.posY[base + i + 1] = cy
      }
    }

    // Pass 2 — draw batched by segment level.
    // Blades are sorted by color so same-colour segments are contiguous;
    // we flush stroke() only on colour change or segment-level change
    // → ~40 stroke() calls per frame instead of 8 000.
    for (let seg = 0; seg < this.SEGMENTS_PER_BLADE; seg++) {
      ctx.lineWidth = 2.5 - ((seg + 1) / this.SEGMENTS_PER_BLADE) * 2

      let currentColor = ''
      let hasPath = false

      for (let b = 0; b < this.blades.length; b++) {
        if (this.blades[b].visibleSegments <= seg) continue

        if (this.blades[b].color !== currentColor) {
          if (hasPath) ctx.stroke()
          ctx.strokeStyle = this.blades[b].color
          ctx.beginPath()
          currentColor = this.blades[b].color
          hasPath = true
        }

        const base = b * this.STRIDE
        ctx.moveTo(this.posX[base + seg], this.posY[base + seg])
        ctx.lineTo(this.posX[base + seg + 1], this.posY[base + seg + 1])
      }

      if (hasPath) ctx.stroke()
    }
  }

  // ── cleanup ───────────────────────────────────────────────────────────

  destroy(): void {
    if (this.animationFrame !== null) {
      cancelAnimationFrame(this.animationFrame)
      this.animationFrame = null
    }
  }
}

// Vue lifecycle hooks
let animation: GrassAnimation | null = null

onMounted(() => {
  setTimeout(() => {
    animation = new GrassAnimation()
    animation.initialize()
  }, 10)
})

onBeforeUnmount(() => {
  if (animation) {
    animation.destroy()
    animation = null
  }
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.hero {
  padding: 8rem 0 6rem;
  background: linear-gradient(135deg, $cream 0%, $warm-beige 100%);
  position: relative;
  overflow: hidden;
  // 96% of viewport height minus navigation bar height (typically 80px)
  min-height: calc(97.4vh - 80px);
  display: flex;
  align-items: center;
  justify-content: center;
}

canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  max-width: 100%;
  max-height: 100%;
  background-color: transparent;
  pointer-events: none;
  z-index: 100;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  position: relative;
  z-index: 2;
  transform: translateY(-40px);
}

.hero-content {
  text-align: center;
  position: relative;
  z-index: 2;
}

.hero-title {
  font-family: $font-family-display;
  font-size: $font-size-hero-large;
  font-weight: $font-weight-bold;
  color: $brown-dark;
  margin-bottom: 1.5rem;
  animation: fadeInUp 0.8s ease forwards;
  letter-spacing: 0.05em;
}

.hero-subtitle {
  font-family: $font-family-base;
  font-size: clamp(1.1rem, 2vw, 1.5rem);
  line-height: 1.6;
  font-weight: $font-weight-regular;
  color: $brown-dark;
  opacity: 0;
  animation: fadeInUp 0.8s ease 0.2s forwards;
}

.hero-circles {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, calc(-50% - 40px));
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  pointer-events: none;
}

.circle-wrapper {
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s ease-out;
}

.radial-glow {
  position: absolute;
  width: 600px;
  height: 600px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, rgba(255, 255, 255, 0) 70%);
  pointer-events: none;
}

.circle {
  border-radius: 50%;
  border: 2px solid;
  opacity: 0.3;

  &-1 {
    width: 280px;
    height: 280px;
    border-color: $green-bright;
    animation: pulse 3s ease-in-out infinite;
  }

  &-2 {
    width: 400px;
    height: 400px;
    border-color: $forest-green;
    animation: pulse 3s ease-in-out 1s infinite;
  }

  &-3 {
    width: 520px;
    height: 520px;
    border-color: $brown-dark;
    animation: pulse 3s ease-in-out 2s infinite;
  }
}

@keyframes pulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.3;
  }
  50% {
    transform: scale(1.03);
    opacity: 0.4;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 968px) {
  .hero {
    padding: 4rem 0 3rem;
    min-height: 60vh;
  }

  .hero-title {
    font-size: clamp(2.5rem, 8vw, 3.5rem);
  }

  .radial-glow {
    width: 430px;
    height: 430px;
  }

  .circle {
    &-1 {
      width: 200px;
      height: 200px;
    }
    &-2 {
      width: 280px;
      height: 280px;
    }
    &-3 {
      width: 360px;
      height: 360px;
    }
  }
}
</style>
