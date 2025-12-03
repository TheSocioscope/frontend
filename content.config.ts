import { defineContentConfig, defineCollection, z } from '@nuxt/content'

export default defineContentConfig({
  collections: {
    pages: defineCollection({
      type: 'page',
      source: 'pages/**/*.md',
      schema: z.object({
        title: z.string(),
        description: z.string().optional(),
        slug: z.string().optional(),
        image: z.string().optional(),
        published: z.boolean().default(true),
        publishedAt: z.date().optional(),
        updatedAt: z.date().optional()
      })
    }),

    // Disabled markdown projects collection to avoid conflict with socioscopeProjects
    // projects: defineCollection({
    //   type: 'page',
    //   source: 'projects/**/*.md',
    //   schema: z.object({
    //     title: z.string(),
    //     description: z.string(),
    //     location: z.string(),
    //     country: z.string(),
    //     image: z.string().optional(),
    //     video: z.string().optional(),
    //     tags: z.array(z.string()).default([]),
    //     featured: z.boolean().default(false),
    //     published: z.boolean().default(true),
    //     publishedAt: z.date().optional()
    //   })
    // }),

    stories: defineCollection({
      type: 'page',
      source: 'stories/**/*.md',
      schema: z.object({
        title: z.string(),
        description: z.string(),
        excerpt: z.string().optional(),
        image: z.string().optional(),
        video: z.string().optional(),
        location: z.string().optional(),
        author: z.string().optional(),
        featured: z.boolean().default(false),
        published: z.boolean().default(true),
        publishedAt: z.date()
      })
    }),

    publications: defineCollection({
      type: 'page',
      source: 'publications/**/*.md',
      schema: z.object({
        title: z.string(),
        authors: z.array(z.string()),
        abstract: z.string(),
        journal: z.string().optional(),
        year: z.number(),
        doi: z.string().optional(),
        url: z.string().optional(),
        pdf: z.string().optional(),
        tags: z.array(z.string()).default([]),
        featured: z.boolean().default(false),
        published: z.boolean().default(true),
        publishedAt: z.date()
      })
    }),

    news: defineCollection({
      type: 'page',
      source: 'news/**/*.md',
      schema: z.object({
        title: z.string(),
        description: z.string(),
        excerpt: z.string().optional(),
        image: z.string().optional(),
        eventDate: z.date().optional(),
        eventLocation: z.string().optional(),
        eventType: z.enum(['news', 'event', 'workshop', 'conference']).default('news'),
        published: z.boolean().default(true),
        publishedAt: z.date()
      })
    }),

    faq: defineCollection({
      type: 'page',
      source: 'faq/**/*.md',
      schema: z.object({
        question: z.string(),
        answer: z.string(),
        category: z.string().optional(),
        order: z.number().default(0),
        published: z.boolean().default(true)
      })
    }),

    partners: defineCollection({
      type: 'page',
      source: 'partners/**/*.md',
      schema: z.object({
        name: z.string(),
        description: z.string(),
        logo: z.string().optional(),
        website: z.string().optional(),
        type: z.enum(['research', 'funding', 'partner']).default('partner'),
        order: z.number().default(0),
        published: z.boolean().default(true)
      })
    }),

    projects: defineCollection({
      type: 'data',
      source: 'projects/*.json',
      schema: z.object({
        pubId: z.number(),
        name: z.string(),
        description: z.string(),
        lang: z.string().optional(),
        location: z.string().optional(),
        url: z.string().optional(),
        yt: z.string().optional(),
        contact: z.object({
          entity: z.string().optional(),
          firstname: z.string().optional(),
          lastname: z.string().optional()
        }).optional(),
        continent: z.array(z.number()).optional(),
        country: z.array(z.number()).optional(),
        field: z.array(z.number()).optional(),
        thematic: z.array(z.number()).optional(),
        type: z.array(z.number()).optional(),
        date: z.array(z.string()).nullable().optional(),
        status: z.number().optional(),
        state: z.number().optional(),
        score: z.number().optional(),
        createdAt: z.number().optional(),
        removedAt: z.number().nullable().optional(),
        team: z.array(z.object({
          entity: z.string().optional(),
          firstname: z.string().optional(),
          lastname: z.string().optional()
        })).optional()
      })
    })
  }
})
