import { defineNitroPlugin } from 'nitropack/runtime/plugin'
import { readdir, readFile, writeFile, mkdir, stat } from 'node:fs/promises'
import { existsSync } from 'node:fs'
import { join } from 'node:path'
import { createHash } from 'node:crypto'
import {
  forceSimulation,
  forceManyBody,
  forceCollide,
  forceX,
  forceY,
  forceCenter
} from 'd3-force'
import { randomLcg } from 'd3-random'

// Galaxy build-time generator (ecosystemGalaxy.md Phase 1)
// Reads content/projects/*.json, runs a deterministic d3-force simulation,
// writes public/data/galaxy-positions.json.
// Determinism: seeded RNG + sorted file order → byte-identical output across builds.
// Cache: hashes content/projects + this script + cluster constants; skips
// the simulation when nothing has changed.

interface SourceProject {
  pubId?: number
  name?: string | Record<string, string>
  continent?: string[]
  sectorFocus?: string[]
  entitySize?: string
}

interface SimNode {
  id: number
  slug: string
  sector: string
  continent: string
  size: 'small' | 'medium' | 'large'
  r: number
  x: number
  y: number
  vx?: number
  vy?: number
}

interface OutputNode {
  id: number
  slug: string
  x: number
  y: number
  r: number
  sector: string
  continent: string
  size: 'small' | 'medium' | 'large'
}

interface SectorEntry {
  key: string
  centroid: [number, number]
}

interface GalaxyOutput {
  version: number
  generatedAt: string
  contentHash: string
  domain: { x: [number, number]; y: [number, number] }
  sectors: SectorEntry[]
  continentColors: Record<string, string>
  nodes: OutputNode[]
}

const CONTINENT_COLORS: Record<string, string> = {
  africa: '#e57373',
  asia: '#ffb74d',
  europe: '#64b5f6',
  'north-america': '#9575cd',
  'south-america': '#4db6ac',
  'latin-america': '#4db6ac',
  oceania: '#a1887f',
  'north-africa': '#f06292',
  'sub-saharian-africa': '#e57373',
  'worldwide-intercontinental': '#90a4ae'
}

const SIZE_RADIUS: Record<string, number> = {
  small: 3,
  medium: 4,
  large: 6
}

// Tunable simulation constants — surfaced here so designers can iterate.
const CENTROID_RADIUS = 280
const CHARGE_STRENGTH = -22
const X_Y_STRENGTH = 0.15
const COLLIDE_PADDING = 1.5
const ALPHA_DECAY = 0.018
const RNG_SEED = 0.1234

const slugify = (text: string) =>
  text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 80)

const resolveName = (raw: string | Record<string, string> | undefined): string => {
  if (!raw) return ''
  if (typeof raw === 'string') return raw
  return raw.en || Object.values(raw)[0] || ''
}

const pickFirst = (arr: string[] | undefined): string | undefined => {
  if (!arr || !Array.isArray(arr) || arr.length === 0) return undefined
  return arr[0]
}

const normalizeSize = (raw: string | undefined): 'small' | 'medium' | 'large' => {
  if (raw === 'small' || raw === 'medium' || raw === 'large') return raw
  return 'medium'
}

export default defineNitroPlugin(async () => {
  const startedAt = Date.now()

  try {
    const projectsDir = join(process.cwd(), 'content/projects')
    const publicDir = join(process.cwd(), 'public')
    const outputPath = join(publicDir, 'data', 'galaxy-positions.json')

    await mkdir(join(publicDir, 'data'), { recursive: true })

    // Sort filenames for deterministic processing order across OSes.
    const files = (await readdir(projectsDir)).filter((f) => f.endsWith('.json')).sort()

    // Build a content hash from each project's mtime + name. Cheaper than
    // reading every file twice. Constants are also folded in so a tuning
    // change forces a rebuild even when content is unchanged.
    const hash = createHash('sha256')
    hash.update(
      JSON.stringify({
        CENTROID_RADIUS,
        CHARGE_STRENGTH,
        X_Y_STRENGTH,
        COLLIDE_PADDING,
        ALPHA_DECAY,
        RNG_SEED,
        version: 1
      })
    )
    for (const file of files) {
      const s = await stat(join(projectsDir, file))
      hash.update(`${file}:${s.size}:${s.mtimeMs}`)
    }
    const contentHash = hash.digest('hex').slice(0, 16)

    // Skip the simulation if the existing JSON already matches this hash.
    if (existsSync(outputPath)) {
      try {
        const existing = JSON.parse(await readFile(outputPath, 'utf-8')) as GalaxyOutput
        if (existing.contentHash === contentHash) {
          console.log(
            `🌌 Galaxy positions cache hit (${existing.nodes.length} nodes) — skipping simulation`
          )
          return
        }
      } catch {
        // Fall through to regenerate
      }
    }

    console.log('🌌 Generating galaxy positions from projects…')

    // Phase A — read + filter to galaxy-eligible projects.
    const nodes: SimNode[] = []
    let skipped = 0
    for (const file of files) {
      const raw = await readFile(join(projectsDir, file), 'utf-8')
      const text = raw.replace(/^﻿/, '')
      let project: SourceProject
      try {
        project = JSON.parse(text)
      } catch {
        skipped++
        continue
      }

      const sector = pickFirst(project.sectorFocus)
      const continent = pickFirst(project.continent)
      if (!sector || !continent || project.pubId == null) {
        skipped++
        continue
      }

      const name = resolveName(project.name)
      const size = normalizeSize(project.entitySize)
      nodes.push({
        id: project.pubId,
        slug: slugify(name),
        sector,
        continent,
        size,
        r: SIZE_RADIUS[size] ?? 4,
        x: 0,
        y: 0
      })
    }

    if (nodes.length === 0) {
      console.warn('🌌 No galaxy-eligible projects found — skipping')
      return
    }

    // Phase B — place sector centroids on a circle of radius CENTROID_RADIUS.
    // Sector order is alphabetical for determinism.
    const sectors = Array.from(new Set(nodes.map((n) => n.sector))).sort()
    const sectorEntries: SectorEntry[] = sectors.map((key, i) => {
      const θ = (i / sectors.length) * Math.PI * 2
      return {
        key,
        centroid: [Math.cos(θ) * CENTROID_RADIUS, Math.sin(θ) * CENTROID_RADIUS]
      }
    })
    const centroidByKey = new Map(sectorEntries.map((s) => [s.key, s.centroid]))

    // Seed initial positions near each node's centroid (small jitter via seeded RNG).
    const rng = randomLcg(RNG_SEED)
    for (const n of nodes) {
      const c = centroidByKey.get(n.sector)!
      n.x = c[0] + (rng() - 0.5) * 20
      n.y = c[1] + (rng() - 0.5) * 20
    }

    // Phase C — run simulation to convergence (synchronous, no animation).
    const sim = forceSimulation<SimNode>(nodes)
      .force('charge', forceManyBody<SimNode>().strength(CHARGE_STRENGTH))
      .force(
        'x',
        forceX<SimNode>((d) => centroidByKey.get(d.sector)![0]).strength(X_Y_STRENGTH)
      )
      .force(
        'y',
        forceY<SimNode>((d) => centroidByKey.get(d.sector)![1]).strength(X_Y_STRENGTH)
      )
      .force('collide', forceCollide<SimNode>((d) => d.r + COLLIDE_PADDING))
      .force('center', forceCenter(0, 0).strength(0.02))
      .alpha(1)
      .alphaDecay(ALPHA_DECAY)
      .randomSource(randomLcg(RNG_SEED))
      .stop()

    // Tick count needed to drive alpha from 1 → alphaMin given alphaDecay.
    const ticks = Math.ceil(
      Math.log(sim.alphaMin() / sim.alpha()) / Math.log(1 - sim.alphaDecay())
    )
    for (let i = 0; i < ticks; i++) sim.tick()

    // Phase D — round positions for stable output and compute domain.
    const round = (v: number) => Math.round(v * 100) / 100
    let minX = Infinity
    let maxX = -Infinity
    let minY = Infinity
    let maxY = -Infinity

    const outputNodes: OutputNode[] = nodes
      .map((n) => {
        const x = round(n.x)
        const y = round(n.y)
        if (x < minX) minX = x
        if (x > maxX) maxX = x
        if (y < minY) minY = y
        if (y > maxY) maxY = y
        return {
          id: n.id,
          slug: n.slug,
          x,
          y,
          r: n.r,
          sector: n.sector,
          continent: n.continent,
          size: n.size
        }
      })
      .sort((a, b) => a.id - b.id) // stable id-sorted ordering for byte-identical output

    const output: GalaxyOutput = {
      version: 1,
      generatedAt: new Date().toISOString(),
      contentHash,
      domain: { x: [round(minX), round(maxX)], y: [round(minY), round(maxY)] },
      sectors: sectorEntries.map((s) => ({
        key: s.key,
        centroid: [round(s.centroid[0]), round(s.centroid[1])]
      })),
      continentColors: CONTINENT_COLORS,
      nodes: outputNodes
    }

    await writeFile(outputPath, JSON.stringify(output, null, 2))

    const elapsed = Date.now() - startedAt
    console.log(
      `🌌 Galaxy positions written: ${outputNodes.length} nodes across ${sectorEntries.length} sectors (${skipped} skipped) in ${elapsed}ms`
    )
  } catch (error) {
    console.error('❌ Error generating galaxy positions:', error)
  }
})
