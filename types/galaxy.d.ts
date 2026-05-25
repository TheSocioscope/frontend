export {}

declare global {
  interface GalaxyNode {
    id: number
    slug: string
    x: number
    y: number
    r: number
    sector: string
    continent: string
    size: 'small' | 'medium' | 'large'
  }

  interface GalaxySector {
    key: string
    centroid: [number, number]
  }

  interface GalaxyData {
    version: number
    generatedAt: string
    contentHash: string
    domain: { x: [number, number]; y: [number, number] }
    sectors: GalaxySector[]
    continentColors: Record<string, string>
    nodes: GalaxyNode[]
  }
}
