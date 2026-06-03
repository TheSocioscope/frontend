<template>
  <section id="timeline" class="project-timeline">
    <span class="section-label">{{ $t('projects.detail.timeline') }}</span>
    <div class="accordion">
      <div v-for="(item, index) in localizedTimeline" :key="index" class="acc-item">
        <button
          type="button"
          class="acc-header"
          :aria-expanded="openItems.has(index)"
          @click="toggle(index)"
        >
          <span class="acc-year" :style="{ color: dateColor(index) }">{{ item.date }}</span>
          <div class="acc-title-wrapper">
            <span class="acc-title">
              {{ item.summary || generateSummary(item.text) }}
            </span>
            <span v-if="openItems.has(index)" class="acc-text">
              {{ item.text }}
            </span>
          </div>
          <v-icon class="acc-chevron" :class="{ open: openItems.has(index) }" size="small">
            mdi-chevron-down
          </v-icon>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const props = defineProps<{
  localizedTimeline: Array<{
    date: string
    text: string
    summary?: string
    icon?: string
    title?: string
  }>
}>()

const { t: $t } = useI18n()

// All items closed on initial load
const openItems = ref<Set<number>>(new Set())

const toggle = (i: number) => {
  const s = new Set(openItems.value)
  if (s.has(i)) s.delete(i)
  else s.add(i)
  openItems.value = s
}

// Cycle blue → pink → green for each date
const DATE_COLORS = ['#85C49A', '#E8C47A', '#C4A890']
const dateColor = (i: number) => DATE_COLORS[i % DATE_COLORS.length]

const generateSummary = (text: string): string => {
  if (!text) return ''

  // Common pattern: "Started doing X" → "Started doing X"
  const startPatterns = [
    /^(Started|Began|Launched|Founded|Created|Established)\s+([^.!?]+[.!?])/i,
    /^(We\s+)?(launched|opened|started|founded|created|established)\s+([^.!?]+[.!?])/i,
  ]

  for (const pattern of startPatterns) {
    const match = text.match(pattern)
    if (match) {
      const captured = match[match.length - 1] || match[2]
      if (captured.length > 8 && captured.length < 120) {
        const verb = match[1] || match[3] || 'Started'
        return `${verb} ${captured}`.trim()
      }
    }
  }

  // Extract first sentence
  const sentenceMatch = text.match(/^([^.!?]*[.!?])/)
  if (sentenceMatch) {
    const sentence = sentenceMatch[1].trim()
    if (sentence.length > 15 && sentence.length < 150) {
      return sentence
    }
  }

  // Try to find dash separator
  const dashIdx = text.indexOf(' — ')
  if (dashIdx > 15 && dashIdx < 120) {
    return text.slice(0, dashIdx).trim()
  }

  // Extract key words and build a natural summary
  // Look for action verbs and important nouns
  const words = text.split(/\s+/)
  const actionVerbs = [
    'expanded', 'opened', 'launched', 'created', 'started', 'began', 'founded',
    'introduced', 'developed', 'implemented', 'established', 'completed', 'finished',
    'achieved', 'reached', 'became', 'grew', 'scaled', 'built', 'partnered'
  ]

  let summary = ''
  let wordCount = 0
  let foundVerb = false

  for (const word of words) {
    const cleanWord = word.toLowerCase().replace(/[,;:]/g, '')

    // Stop at end of first sentence
    if (summary && (word.endsWith('.') || word.endsWith('!') || word.endsWith('?'))) {
      summary += ' ' + word
      break
    }

    // Limit to a reasonable length
    if (wordCount >= 15) {
      if (!summary.endsWith('.')) summary += '.'
      break
    }

    if (actionVerbs.includes(cleanWord)) {
      foundVerb = true
    }

    summary += (summary ? ' ' : '') + word
    wordCount++

    // If we found a verb and have a few more words, we might have a good summary
    if (foundVerb && wordCount >= 8) {
      break
    }
  }

  // Ensure it ends with proper punctuation
  const trimmed = summary.trim()
  if (!trimmed.endsWith('.') && !trimmed.endsWith('!') && !trimmed.endsWith('?')) {
    return trimmed + '.'
  }

  return trimmed
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-timeline {
  margin-bottom: $rhythm-4;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $rhythm-2;
}

.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $text-secondary;
  margin-bottom: $rhythm-2;
}

.accordion {
  border-top: 0.5px solid $border-soft;
}

.acc-item {
  border-bottom: 0.5px solid $border-soft;

  &:last-child {
    border-bottom: none;
  }
}

.acc-header {
  display: grid;
  grid-template-columns: 130px 1fr auto;
  column-gap: $rhythm-3;
  align-items: start;
  width: 100%;
  padding: 14px 4px;
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  font-family: $font-family-base;

  &:hover .acc-title {
    color: $green-forest;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
  }
}

.acc-year {
  font-family: $font-family-display;
  font-size: 1.25rem;
  font-weight: $font-weight-semibold;
  white-space: nowrap;
  line-height: 1.4;
}

.acc-title-wrapper {
  display: flex;
  flex-direction: column;
  gap: 8px;
  min-width: 0;
  flex: 1;
}

.acc-title {
  font-size: 14px;
  font-weight: 700;
  color: $text-primary;
  min-width: 0;
  line-height: 1.5;
  transition: color $transition-fast;
}

.acc-text {
  font-size: 13px;
  font-weight: 400;
  color: $text-secondary;
  line-height: 1.6;
  white-space: normal;
}

.acc-chevron {
  color: $text-caption;
  transition: transform 0.2s ease;
  margin-top: 2px;

  &.open {
    transform: rotate(180deg);
  }
}
</style>
