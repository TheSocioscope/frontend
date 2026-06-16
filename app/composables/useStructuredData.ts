export const useStructuredData = () => {
  const useHeadFn = useHead

  const organizationSchema = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'The Socioscope',
    url: 'https://thesocioscope.org',
    logo: 'https://thesocioscope.org/logo.png',
    description: 'Seeing How Societies Transform. Exploring sustainable food initiatives and strategic research insights.',
    sameAs: [
      'https://www.facebook.com/thesocioscope',
      'https://www.twitter.com/thesocioscope',
      'https://www.instagram.com/thesocioscope',
      'https://www.linkedin.com/company/thesocioscope'
    ],
    contactPoint: {
      '@type': 'ContactPoint',
      email: 'info@thesocioscope.org',
      contactType: 'Customer Support'
    }
  }

  const websiteSchema = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    url: 'https://thesocioscope.org',
    name: 'The Socioscope',
    description: 'Seeing How Societies Transform',
    potentialAction: {
      '@type': 'SearchAction',
      target: 'https://thesocioscope.org/projects?q={search_term_string}',
      'query-input': 'required name=search_term_string'
    }
  }

  const addOrganizationSchema = () => {
    useHeadFn({
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify(organizationSchema)
        }
      ]
    })
  }

  const addWebsiteSchema = () => {
    useHeadFn({
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify(websiteSchema)
        }
      ]
    })
  }

  const addBreadcrumbSchema = (items: Array<{ name: string; url: string }>) => {
    const breadcrumb = {
      '@context': 'https://schema.org',
      '@type': 'BreadcrumbList',
      itemListElement: items.map((item, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        name: item.name,
        item: item.url
      }))
    }

    useHeadFn({
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify(breadcrumb)
        }
      ]
    })
  }

  return {
    addOrganizationSchema,
    addWebsiteSchema,
    addBreadcrumbSchema
  }
}
