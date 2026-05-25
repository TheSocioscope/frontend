<template>
  <div>
    <div class="resources-grid">
      <a
        v-for="resource in filteredResources"
        :key="resource._path"
        :href="resource.link"
        target="_blank"
        rel="noopener noreferrer"
        class="resource-card"
      >
        <div class="resource-meta">
          <span class="resource-category">{{ getCategoryLabel(resource.category) }}</span>
          <span v-if="resource.date" class="resource-date">{{ resource.date }}</span>
        </div>
        <div class="resource-heading">
          <h3>{{ resource.title }}</h3>
          <span class="resource-arrow" aria-hidden="true">
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
        </div>
        <p v-if="resource.authors" class="resource-authors">{{ resource.authors }}</p>
        <p v-if="resource.abstract" class="resource-abstract">{{ resource.abstract }}</p>
      </a>
    </div>

    <div v-if="filteredResources.length === 0" class="empty-state">
      <p>{{ $t('resources.noResults') }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t } = useI18n()

const props = defineProps<{
  resources: any[]
  activeFilter: string
  searchQuery: string
}>()

const filteredResources = computed(() => {
  let filtered = props.resources

  // Filter by category
  if (props.activeFilter !== 'all') {
    filtered = filtered.filter((r) => r.category === props.activeFilter)
  }

  // Filter by search query
  if (props.searchQuery) {
    const query = props.searchQuery.toLowerCase()
    filtered = filtered.filter(
      (r) =>
        r.title?.toLowerCase().includes(query) ||
        r.abstract?.toLowerCase().includes(query) ||
        (r.authors && r.authors.toLowerCase().includes(query))
    )
  }

  return filtered
})

const getCategoryLabel = (category: string) => {
  const labels: Record<string, string> = {
    article: t('resources.categoryLabels.article'),
    book: t('resources.categoryLabels.book'),
    event: t('resources.categoryLabels.event'),
    funding: t('resources.categoryLabels.funding'),
    organization: t('resources.categoryLabels.organization'),
    policy: t('resources.categoryLabels.policy'),
    socioscope: t('resources.categoryLabels.socioscope')
  }
  return labels[category] || category
}

const getLinkText = (category: string) => {
  const linkTexts: Record<string, string> = {
    article: t('resources.linkTexts.article'),
    book: t('resources.linkTexts.book'),
    event: t('resources.linkTexts.event'),
    funding: t('resources.linkTexts.funding'),
    organization: t('resources.linkTexts.organization'),
    policy: t('resources.linkTexts.policy'),
    socioscope: t('resources.linkTexts.socioscope')
  }
  return linkTexts[category] || t('resources.linkTexts.default')
}
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;

  /* Mobile: 2-up tile grid (matches products + team aesthetic). */
  @media (max-width: 600px) {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
}

/* Whole card is the link — sleeker than a separate "Read article" CTA
   line at the bottom. Hover lifts the card and fills the arrow chip
   with green, matching the products + team pattern. */
.resource-card {
  background: white;
  padding: 1rem 1.125rem 1.125rem;
  border-radius: 8px;
  border: 1px solid $border-cream;
  text-decoration: none;
  color: inherit;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(44, 36, 22, 0.08);
    border-color: $green-bright;

    .resource-arrow {
      background: $green-bright;
      border-color: $green-bright;
      color: white;
    }
  }

  &:focus-visible {
    outline: 2px solid $green-bright;
    outline-offset: 2px;
  }

  h3 {
    font-family: $font-family-display;
    font-size: 1.0625rem;
    font-weight: 600;
    color: $brown-dark;
    margin: 0;
    line-height: 1.3;
    flex: 1;
    min-width: 0;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;

    @media (max-width: 600px) {
      font-size: 0.875rem;
      line-height: 1.25;
      -webkit-line-clamp: 3;
    }
  }

  @media (max-width: 600px) {
    padding: 0.625rem 0.75rem 0.75rem;
    gap: 0.25rem;
  }
}

/* Below ~360px (very narrow phones) the 2-up grid gets cramped. Fall
   back to a single column where each card has room to breathe. */
@media (max-width: 360px) {
  .resources-grid {
    grid-template-columns: 1fr;
  }
}

.resource-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.5rem;
  flex-wrap: wrap;

  @media (max-width: 600px) {
    /* On 2-up phone tiles, gap shrinks so the meta row stays one line. */
    gap: 0.25rem;
  }
}

.resource-date {
  font-size: 0.6875rem;
  color: $text-caption;
  font-weight: 500;
  letter-spacing: 0.02em;

  @media (max-width: 600px) {
    font-size: 0.625rem;
  }
}

.resource-category {
  display: inline-flex;
  align-items: center;
  padding: 0.125rem 0.5rem;
  background: rgba(76, 160, 73, 0.1);
  color: $forest-green;
  font-size: 0.625rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-radius: 999px;

  @media (max-width: 600px) {
    font-size: 0.5625rem;
    letter-spacing: 0.06em;
    padding: 0.0625rem 0.4375rem;
  }
}

.resource-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
}

.resource-arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border: 1px solid rgba(44, 36, 22, 0.2);
  border-radius: 4px;
  color: $brown-dark;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;

  @media (max-width: 600px) {
    width: 24px;
    height: 24px;
  }
}

.resource-authors {
  color: $forest-green;
  font-weight: 600;
  font-size: 0.8125rem;
  margin: 0;

  @media (max-width: 600px) {
    font-size: 0.75rem;
  }
}

.resource-abstract {
  color: $brown-dark;
  opacity: 0.78;
  font-size: 0.875rem;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;

  @media (max-width: 600px) {
    font-size: 0.75rem;
    line-height: 1.45;
    -webkit-line-clamp: 2;
  }
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: $brown-dark;
  opacity: 0.6;

  p {
    font-size: 1rem;
  }
}
</style>
