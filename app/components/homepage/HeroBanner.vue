<template>
  <section class="hero">
    <canvas id="canvas"></canvas>
    <!-- Animated Circles Background -->
    <div class="hero-circles">
      <div class="circle circle-1" />
      <div class="circle circle-2" />
      <div class="circle circle-3" />
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
import { onMounted, onBeforeUnmount } from 'vue'

const { t: $t } = useI18n()

// Simplified Grass Animation
// Draws grass blades from bottom to top over 30 seconds

interface GrassBlade {
  x: number
  y: number
  angle: number
  segments: Array<{ x: number; y: number }>
  currentSegment: number
  maxSegments: number
  color: string
}

class GrassAnimation {
  private canvas: HTMLCanvasElement | null = null
  private context: CanvasRenderingContext2D | null = null
  private canvasWidth = 0
  private canvasHeight = 0
  private dpi = 1
  private blades: GrassBlade[] = []
  private readonly MAX_BLADES = 800
  private readonly SEGMENTS_PER_BLADE = 10
  private drawInterval: number | null = null
  private animationTimeout: number | null = null
  private readonly ANIMATION_DURATION = 30000 // 30 seconds

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

    // Start animation
    this.drawInterval = window.setInterval(() => this.draw(), 150)
    this.animationTimeout = window.setTimeout(() => this.stopAnimation(), this.ANIMATION_DURATION)
  }

  private draw(): void {
    // Grow existing blades
    for (const blade of this.blades) {
      if (blade.currentSegment < blade.maxSegments) {
        this.drawBladeSegment(blade)
        blade.currentSegment++
      }
    }

    // Add new blades if we haven't reached max (create 12 per cycle for better distribution)
    for (let i = 0; i < 12 && this.blades.length < this.MAX_BLADES; i++) {
      this.createGrassBlade()
    }
  }

  private createGrassBlade(): void {
    const x = Math.random() * this.canvasWidth
    const y = this.canvasHeight + 5
    const angle = -Math.PI / 2 + (Math.random() - 0.5) * (Math.PI / 8) // Upward with ±22.5° variation
    const height = Math.random() * 40 + 30 // 30-70px tall

    // Randomize color: 50% get #4ca049, rest random among the other 3
    let color: string
    if (Math.random() < 0.5) {
      color = '#4ca049' // green-bright
    } else {
      const otherColors = ['#4caf50', '#6b8e23', '#8fbc8f'] // green-medium, green-olive, green-light-olive
      color = otherColors[Math.floor(Math.random() * otherColors.length)]
    }

    const blade: GrassBlade = {
      x,
      y,
      angle,
      segments: [],
      currentSegment: 0,
      maxSegments: this.SEGMENTS_PER_BLADE,
      color
    }

    // Pre-calculate all segments for smooth curve
    const segmentLength = height / this.SEGMENTS_PER_BLADE
    let currentX = x
    let currentY = y
    let currentAngle = angle

    for (let i = 0; i < this.SEGMENTS_PER_BLADE; i++) {
      // Add slight curve variation as blade grows
      currentAngle += (Math.random() - 0.5) * 0.1
      currentX += Math.cos(currentAngle) * segmentLength
      currentY += Math.sin(currentAngle) * segmentLength

      blade.segments.push({ x: currentX, y: currentY })
    }

    this.blades.push(blade)
  }

  private drawBladeSegment(blade: GrassBlade): void {
    if (!this.context || blade.currentSegment === 0) return

    const segment = blade.segments[blade.currentSegment]
    const prevSegment =
      blade.currentSegment === 0
        ? { x: blade.x, y: blade.y }
        : blade.segments[blade.currentSegment - 1]

    this.context.strokeStyle = blade.color
    // Taper: wider at base (early segments), narrower at top (later segments)
    const progress = blade.currentSegment / blade.maxSegments
    this.context.lineWidth = 2.5 - progress * 2 // 2.5 at start, 0.5 at end
    this.context.lineCap = 'round'
    this.context.beginPath()
    this.context.moveTo(prevSegment.x, prevSegment.y)
    this.context.lineTo(segment.x, segment.y)
    this.context.stroke()
  }

  private stopAnimation(): void {
    if (this.drawInterval !== null) {
      window.clearInterval(this.drawInterval)
      this.drawInterval = null
    }
  }

  destroy(): void {
    this.stopAnimation()
    if (this.animationTimeout !== null) {
      window.clearTimeout(this.animationTimeout)
      this.animationTimeout = null
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
  min-height: calc(96vh - 80px);
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

.circle {
  position: absolute;
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
    transform: scale(1.1);
    opacity: 0.5;
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
