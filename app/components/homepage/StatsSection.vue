<template>
  <section class="metrics">
    <div class="container">
      <div class="metrics-grid">
        <div v-for="(stat, index) in stats" :key="index" class="metric-card">
          <div class="metric-number">
            <span v-if="isVisible">{{ animatedValues[index] }}</span>
            <span v-else>{{ stat.number }}</span>
          </div>
          <div class="metric-label">{{ stat.label }}</div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
interface OverallStats {
  totalProjects: number
  totalCountries: number
}

const { t: $t } = useI18n()
const config = useRuntimeConfig()

// Load real stats
const overallStats = ref<OverallStats | null>(null)

onMounted(async () => {
  try {
    const baseURL = config.app.baseURL || '/'
    const response = await fetch(`${baseURL}data/overall-stats.json`)
    overallStats.value = await response.json()
    console.log('Loaded overall stats:', overallStats.value)
  } catch (error) {
    console.error('Error loading overall stats:', error)
  }
})

const stats = computed(() => {
  if (!overallStats.value) {
    // Return placeholder values while loading
    return [
      {
        number: '...',
        label: $t('stats.card1.label'),
        target: 0
      },
      {
        number: '...',
        label: $t('stats.card2.label'),
        target: 0
      },
      {
        number: '...',
        label: $t('stats.card4.label'),
        target: 0
      },
      {
        number: '...',
        label: $t('stats.card3.label'),
        target: 0
      }
    ]
  }

  return [
    {
      number: `${overallStats.value.totalProjects}+`,
      label: $t('stats.card1.label'),
      target: overallStats.value.totalProjects
    },
    {
      number: `${overallStats.value.totalCountries}+`,
      label: $t('stats.card2.label'),
      target: overallStats.value.totalCountries
    },
    {
      number: '50+',
      label: $t('stats.card4.label'),
      target: 50
    },
    {
      number: '6',
      label: $t('stats.card3.label'),
      target: 6
    }
  ]
})

const isVisible = ref(false)
const animatedValues = ref(['0', '0', '0', '0'])

const animateValue = (index: number, start: number, end: number, duration: number) => {
  const startTime = Date.now()
  const isPlus = stats.value[index].number.includes('+')

  const updateValue = () => {
    const currentTime = Date.now()
    const elapsed = currentTime - startTime
    const progress = Math.min(elapsed / duration, 1)

    const current = Math.floor(start + (end - start) * progress)
    animatedValues.value[index] = isPlus ? `${current}+` : current.toString()

    if (progress < 1) {
      requestAnimationFrame(updateValue)
    }
  }

  requestAnimationFrame(updateValue)
}

onMounted(() => {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !isVisible.value) {
          isVisible.value = true
          stats.value.forEach((stat, index) => {
            animateValue(index, 0, stat.target, 2000)
          })
        }
      })
    },
    { threshold: 0.5 }
  )

  const section = document.querySelector('.metrics')
  if (section) {
    observer.observe(section)
  }
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.metrics {
  background: $green-bright;
  color: $cream;
  padding: 4rem 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 2rem;
  text-align: center;

  @media (max-width: 968px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.metric-card {
  padding: 1rem;
}

.metric-number {
  font-family: $font-family-display;
  font-size: 3.5rem;
  font-weight: $font-weight-bold;
  color: $cream;
  margin-bottom: 0.5rem;
  line-height: 1.2;

  @media (max-width: 968px) {
    font-size: 2.5rem;
  }
}

.metric-label {
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: $warm-beige;
}
</style>
