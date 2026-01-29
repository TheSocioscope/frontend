<template>
  <div>
    <div class="results-info">
      {{ $t('resources.resultsInfo', { count: filteredResources.length }) }}
    </div>

    <div class="resources-grid">
      <article v-for="resource in filteredResources" :key="resource._path" class="resource-card">
        <div class="resource-meta">
          <span class="resource-date">{{ resource.date }}</span>
          <span class="resource-category">{{ getCategoryLabel(resource.category) }}</span>
        </div>
        <h3>{{ resource.title }}</h3>
        <p v-if="resource.authors" class="resource-authors">{{ resource.authors }}</p>
        <p class="resource-abstract">{{ resource.abstract }}</p>
        <a :href="resource.link" target="_blank" rel="noopener noreferrer" class="resource-link">
          {{ getLinkText(resource.category) }}
        </a>
      </article>
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

.results-info {
  text-align: center;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  color: $brown-dark;
  opacity: 0.8;
}

.resources-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.resource-card {
  background: white;
  padding: 2rem;
  border-radius: $border-radius-lg;
  border: 2px solid $border-cream;
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    border-color: $green-bright;
  }

  h3 {
    font-family: $font-family-display;
    font-size: 1.5rem;
    color: $brown-dark;
    margin-bottom: 0.75rem;
    line-height: 1.3;
  }
}

.resource-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 1rem;
  flex-wrap: wrap;
}

.resource-date {
  font-size: 0.9rem;
  color: $brown-dark;
  opacity: 0.7;
}

.resource-category {
  background: $green-bright;
  color: white;
  padding: 0.35rem 1rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.resource-authors {
  color: $green-bright;
  font-weight: 600;
  margin-bottom: 0.75rem;
  font-size: 0.95rem;
}

.resource-abstract {
  color: $brown-dark;
  opacity: 0.8;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.resource-link {
  color: $green-bright;
  font-weight: 600;
  text-decoration: none;
  transition: all 0.3s ease;
  display: inline-block;

  &:hover {
    transform: translateX(5px);
    opacity: 0.8;
  }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: $brown-dark;
  opacity: 0.6;

  p {
    font-size: 1.25rem;
  }
}
</style>
