# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
yarn install       # Install dependencies
yarn dev           # Start dev server at http://localhost:3000
yarn build         # Build for production
yarn generate      # Static site generation (SSG) — used for deployment
yarn preview       # Preview production build locally
```

No lint or test scripts are configured. ESLint is integrated as a Nuxt module and runs during build.

## Architecture

**Nuxt 4 static site** deployed to GitHub Pages at `thesocioscope.github.io/frontend`. The production base path is `/frontend/` with trailing slashes enabled.

**Key modules:**
- **Nuxt Content 3** — Markdown/JSON content in `/content`, with Zod schema validation defined in `content.config.ts`
- **@nuxtjs/i18n** — 4 languages (en default, fr, es, de) using `prefix_except_default` strategy; translation JSON files in `/i18n/locales/`
- **Vuetify 3** — initialized as a Nuxt plugin in `/app/plugins/vuetify.ts`
- **@nuxt/image** — image optimization; production paths resolve via `useImagePath` composable
- **Decap CMS** — Git-based editorial interface, config in `/public/admin/`
- **D3.js** — interactive world map visualization

**Directory layout:**
- `/app` — Vue application code (components, composables, layouts, pages, plugins)
- `/content` — Markdown stories, JSON projects database, FAQ, team, partners, products, resources, pages
- `/i18n/locales` — Translation JSON files + Python helper scripts for translation management
- `/public` — Static assets, images, data files
- `/server` — Nuxt server API routes
- `/types` — TypeScript type definitions (`content.d.ts`)

**Content collections** (defined in `content.config.ts`): `stories`, `faq`, `team`, `partners`, `products`, `resources`, `projects`

## Key Patterns

**Localized content queries** — use the `useLocalizedCollection` composable instead of querying Nuxt Content directly, to handle locale-aware content fetching.

**Image paths** — use the `useImagePath` composable for image path resolution, which handles the `/frontend/` base path in production.

**Static constants** (social media links, contact info) — defined in `static.config.ts` at the root.

**Formatting** — Prettier is configured (`.prettierrc`): 100-char line width, single quotes, no semicolons.
