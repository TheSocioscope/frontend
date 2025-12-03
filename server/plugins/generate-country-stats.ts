import { defineNitroPlugin } from 'nitropack/runtime/plugin'
import { readdir, readFile, writeFile, mkdir } from 'node:fs/promises'
import { join } from 'node:path'

interface Project {
  country?: string[]
  pubId: number
  name: string
  status?: string
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

interface OverallStats {
  totalProjects: number
  totalCountries: number
}

export default defineNitroPlugin(async (nitroApp) => {
  console.log('🗺️  Generating country statistics from projects...')

  try {
    const projectsDir = join(process.cwd(), 'content/projects')
    const publicDir = join(process.cwd(), 'public')
    const outputPath = join(publicDir, 'data', 'country-stats.json')

    // Ensure output directory exists
    await mkdir(join(publicDir, 'data'), { recursive: true })

    // Read all project files
    const files = await readdir(projectsDir)
    const jsonFiles = files.filter((file) => file.endsWith('.json'))

    const countryStats: CountryStats = {}

    // Process each project
    for (const file of jsonFiles) {
      const content = await readFile(join(projectsDir, file), 'utf-8')
      const project: Project = JSON.parse(content)

      if (project.country && Array.isArray(project.country)) {
        for (const countryCode of project.country) {
          if (!countryStats[countryCode]) {
            countryStats[countryCode] = {
              count: 0,
              projects: []
            }
          }

          countryStats[countryCode].count++
          countryStats[countryCode].projects.push({
            pubId: project.pubId,
            name: project.name
          })
        }
      }
    }

    // Calculate overall stats
    const overallStats: OverallStats = {
      totalProjects: jsonFiles.length,
      totalCountries: Object.keys(countryStats).length
    }

    // Write the stats files
    await writeFile(outputPath, JSON.stringify(countryStats, null, 2))
    await writeFile(
      join(publicDir, 'data', 'overall-stats.json'),
      JSON.stringify(overallStats, null, 2)
    )

    console.log(
      `✅ Generated statistics: ${overallStats.totalProjects} projects, ${overallStats.totalCountries} countries`
    )
  } catch (error) {
    console.error('❌ Error generating country statistics:', error)
  }
})
