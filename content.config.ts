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

    team: defineCollection({
      type: 'page',
      source: 'team/**/*.md',
      schema: z.object({
        firstname: z.string(),
        lastname: z.string(),
        picture: z.string().optional(),
        country: z.string(),
        category: z.string(),
        role: z.string(),
        details: z.string().optional()
      })
    }),

    partners: defineCollection({
      type: 'page',
      source: 'partners/**/*.md',
      schema: z.object({
        title: z.string().optional(),
        name: z.string().optional(),
        description: z.string().optional(),
        category: z.string().optional(),
        logo: z.string().optional(),
        website: z.string().optional(),
        type: z.enum(['research', 'funding', 'partner']).optional(),
        order: z.number().default(0),
        published: z.boolean().default(true),
        partners: z
          .array(
            z.object({
              name: z.string(),
              country: z.string(),
              logo: z.string().optional(),
              website: z.string().optional(),
              role: z.string()
            })
          )
          .optional()
      })
    }),

    interviewers: defineCollection({
      type: 'page',
      source: 'interviewers/**/*.md',
      schema: z.object({
        title: z.string(),
        description: z.string(),
        category: z.string(),
        searchable: z.boolean().optional(),
        interviewers: z.array(
          z.object({
            name: z.string(),
            country: z.string(),
            picture: z.string().optional()
          })
        )
      })
    }),

    products: defineCollection({
      type: 'page',
      source: 'products/**/*.md',
      schema: z.object({
        title: z.string(),
        producer: z.string(),
        category: z.string(),
        badge: z.string(),
        icon: z.string(),
        description: z.string(),
        link: z.string(),
        order: z.number().default(0),
        published: z.boolean().default(true)
      })
    }),

    resources: defineCollection({
      type: 'page',
      source: 'resources/**/*.md',
      schema: z.object({
        title: z.string(),
        authors: z.string().optional(),
        category: z.enum([
          'article',
          'book',
          'event',
          'funding',
          'organization',
          'policy',
          'socioscope'
        ]),
        date: z.string(),
        abstract: z.string(),
        link: z.string(),
        order: z.number().default(0),
        published: z.boolean().default(true)
      })
    }),

    projects: defineCollection({
      type: 'data',
      source: 'projects/*.json',
      schema: z.object({
        pubId: z.number(),
        name: z.union([
          z.string(),
          z.object({
            en: z.string(),
            fr: z.string(),
            es: z.string(),
            de: z.string()
          })
        ]),
        description: z.union([
          z.string(),
          z.object({
            en: z.string(),
            fr: z.string(),
            es: z.string(),
            de: z.string()
          })
        ]),
        originalLang: z.string().optional(),
        lang: z.string().optional(),
        location: z.string().optional(),
        url: z.string().optional(),
        yt: z.string().optional(),
        contact: z
          .object({
            entity: z.string().optional(),
            firstname: z.string().optional(),
            lastname: z.string().optional()
          })
          .optional(),
        continent: z.array(z.string()).optional(),
        country: z.array(z.string()).optional(),
        field: z.array(z.string()).optional(),
        thematic: z.array(z.string()).optional(),
        type: z.array(z.string()).optional(),
        date: z.array(z.string()).nullable().optional(),
        status: z.string().optional(),
        state: z.string().optional(),
        score: z.number().optional(),
        createdAt: z.number().optional(),
        removedAt: z.number().nullable().optional(),
        team: z
          .array(
            z.object({
              entity: z.string().optional(),
              firstname: z.string().optional(),
              lastname: z.string().optional()
            })
          )
          .optional()
      })
    })
  }
})
