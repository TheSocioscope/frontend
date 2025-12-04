// Global type augmentation for Nuxt Content
// This file extends the auto-generated types from @nuxt/content

export {}

declare global {
  // Extend project collection item with multilingual fields
  interface ProjectItem {
    originalLang?: string
    name: string | Record<string, string>
    description?: string | Record<string, string>
    periodicity?: string
    pubId: number
    stem: string
    status?: string | number
    location?: string
    continent?: string[]
    country?: string[]
    field?: string[]
    thematic?: string[]
    type?: string[]
    state?: string
    lang?: string
    yt?: string
    url?: string
    score?: number
    createdAt?: number
    contact?: Record<string, string>
    date?: string[]
    team?: Array<Record<string, string>>
  }
}
