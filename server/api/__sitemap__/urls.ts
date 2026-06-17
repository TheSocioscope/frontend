import { defineSitemapEventHandler, asSitemapUrl } from '#imports'
import { readdir, readFile } from 'node:fs/promises'
import { join } from 'node:path'

const slugify = (text: string) =>
  text
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, 80)

export default defineSitemapEventHandler(async () => {
  const projectsDir = join(process.cwd(), 'content', 'projects')
  const files = await readdir(projectsDir)

  const urls = []
  for (const file of files) {
    if (!file.endsWith('.json')) continue
    const raw = await readFile(join(projectsDir, file), 'utf-8')
    const project = JSON.parse(raw)
    const name = typeof project.name === 'string' ? project.name : project.name?.en || ''
    if (!name) continue
    const slug = slugify(name)
    if (!slug) continue
    urls.push(
      asSitemapUrl({
        loc: `/projects/${slug}/`,
        changefreq: 'monthly',
        priority: 0.7,
      })
    )
  }

  return urls
})