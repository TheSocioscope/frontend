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

interface InterviewerFile {
  interviewers?: Array<{
    name: string
    country?: string
    picture?: string
  }>
}

interface OverallStats {
  totalProjects: number
  totalCountries: number
  totalInterviewers: number
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

    // Count interviewers from markdown files
    let totalInterviewers = 0
    try {
      const interviewersDir = join(process.cwd(), 'content/interviewers')
      const interviewerFiles = await readdir(interviewersDir)
      const mdFiles = interviewerFiles.filter((file) => file.endsWith('.md'))

      for (const file of mdFiles) {
        const content = await readFile(join(interviewersDir, file), 'utf-8')
        // Extract frontmatter
        const frontmatterMatch = content.match(/^---\n([\s\S]*?)\n---/)
        if (frontmatterMatch) {
          const frontmatter = frontmatterMatch[1]
          // Count interviewers in the interviewers array
          const interviewerMatches = frontmatter.match(/- name:/g)
          if (interviewerMatches) {
            totalInterviewers += interviewerMatches.length
          }
        }
      }
    } catch (error) {
      console.error('❌ Error counting interviewers:', error)
    }

    // Calculate overall stats
    const overallStats: OverallStats = {
      totalProjects: jsonFiles.length,
      totalCountries: Object.keys(countryStats).length,
      totalInterviewers
    }

    // Write the stats files
    await writeFile(outputPath, JSON.stringify(countryStats, null, 2))
    await writeFile(
      join(publicDir, 'data', 'overall-stats.json'),
      JSON.stringify(overallStats, null, 2)
    )

    console.log(
      `✅ Generated statistics: ${overallStats.totalProjects} projects, ${overallStats.totalCountries} countries, ${overallStats.totalInterviewers} interviewers`
    )
  } catch (error) {
    console.error('❌ Error generating country statistics:', error)
  }
})
