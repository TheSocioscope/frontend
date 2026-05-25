<template>
  <section class="partners-section">
    <v-container>
      <div class="partners-grid">
        <header class="partners-header section-reveal">
          <h2 class="partners-title">{{ $t('leadingResearch.title') }}</h2>
          <p class="partners-support">{{ $t('leadingResearch.nomis') }}</p>
        </header>
        <ul class="partners-list section-reveal">
          <li v-for="(partner, index) in displayedPartners" :key="index" class="partner-item">
            <a
              class="partner-link"
              :href="partner.url"
              target="_blank"
              rel="noopener noreferrer"
            >
              <div class="partner-content">
                <h3 class="partner-title">{{ partner.title }}</h3>
                <p class="partner-lead">
                  <strong class="partner-lead-name">{{ splitLead(partner.lead).name }}</strong>
                  <span v-if="splitLead(partner.lead).role">{{ splitLead(partner.lead).role }}</span>
                </p>
              </div>
              <span class="partner-arrow" aria-hidden="true">
                <svg viewBox="0 0 24 24" width="14" height="14">
                  <path
                    d="M5 12h14M13 6l6 6-6 6"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  />
                </svg>
              </span>
            </a>
          </li>
        </ul>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t, locale } = useI18n()

// Fallback partners from i18n
const fallbackPartners = [
  {
    title: 'Complexity Science Hub Vienna',
    lead: 'Helga Nowotny, Project Lead',
    url: 'https://csh.ac.at/'
  },
  {
    title: 'Paris Institute for Advanced Study',
    lead: 'Saadi Lahlou, Project Lead',
    url: 'https://www.paris-iea.fr/en'
  }
]

// Fetch partners from content
const { data: partners } = await useAsyncData(
  'partners',
  async () => {
    try {
      const content = await queryContent(`partners/${locale.value}`)
        .where({ published: true })
        .sort({ order: 1 })
        .find()
      return content
    } catch (e) {
      return null
    }
  },
  { watch: [locale], default: () => null }
)

/* Split "Helga Nowotny, Project Lead" → { name: "Helga Nowotny", role: ", Project Lead" }.
   The leading comma is kept on the role so the bold name flows naturally into the rest. */
const splitLead = (lead?: string) => {
  if (!lead) return { name: '', role: '' }
  const idx = lead.indexOf(',')
  if (idx === -1) return { name: lead, role: '' }
  return { name: lead.slice(0, idx), role: lead.slice(idx) }
}

const displayedPartners = computed(() => {
  if (partners.value && Array.isArray(partners.value) && partners.value.length > 0) {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    return partners.value.map((p: any) => ({
      title: p.title,
      lead: p.lead,
      url: p.url
    }))
  }
  return fallbackPartners
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.partners-section {
  background: $surface-cream;
  padding: 3.5rem 0;

  @media (max-width: 768px) {
    padding: 2rem 0;
  }
}

/* Centered header — title + nomis credit sit above the partner list,
   capped so the lines don't sprawl across the wide container. */
.partners-grid {
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.partners-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.75rem;
  max-width: 760px;
  margin: 0 auto;
}

.partners-title {
  font-family: $font-family-display;
  font-size: 2rem;
  font-weight: $font-weight-bold;
  color: $brown-dark;
  line-height: 1.15;
  margin: 0;

  @media (max-width: 768px) {
    font-size: 1.5rem;
  }
}

.partners-support {
  font-size: 0.9375rem;
  font-style: italic;
  line-height: 1.55;
  color: $brown-medium;
  margin: 0;

  @media (max-width: 768px) {
    font-size: 0.875rem;
  }
}

.partners-list {
  list-style: none;
  margin: 0 auto;
  padding: 0;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 0.75rem;
  max-width: 880px;
  width: 100%;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.partner-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1rem 1.125rem;
  background: white;
  border: 1px solid $cream-dark;
  border-radius: 6px;
  text-decoration: none;
  color: inherit;
  transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;

  &:hover,
  &:focus-visible {
    border-color: $green-bright;
    transform: translateX(2px);
    box-shadow: 0 4px 14px rgba(44, 36, 22, 0.06);
  }

  &:focus-visible {
    outline: 2px solid $green-bright;
    outline-offset: 2px;
  }
}

.partner-content {
  min-width: 0;
}

.partner-title {
  font-family: $font-family-display;
  font-size: 1.0625rem;
  font-weight: 600;
  color: $green-bright;
  margin: 0 0 0.125rem;
  line-height: 1.3;
}

.partner-lead {
  font-size: 0.875rem;
  line-height: 1.45;
  color: $brown-dark;
  opacity: 0.8;
  margin: 0;
  font-family: $font-family-display;
}

.partner-lead-name {
  font-weight: $font-weight-bold;
}

.partner-arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border: 1px solid rgba(44, 36, 22, 0.2);
  border-radius: 4px;
  color: $brown-dark;
  transition: background 0.2s ease, color 0.2s ease;
}

.partner-link:hover .partner-arrow,
.partner-link:focus-visible .partner-arrow {
  background: $green-bright;
  border-color: $green-bright;
  color: white;
}
</style>
