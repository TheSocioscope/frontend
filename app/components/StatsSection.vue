<template>
  <section class="stats-section gradient-green">
    <v-container>
      <v-row>
        <v-col v-for="(stat, index) in stats" :key="index" cols="12" md="4">
          <div class="stat-card">
            <div class="text-h2 text-md-h1 font-weight-bold stat-number">
              <span v-if="isVisible">{{ animatedValues[index] }}</span>
              <span v-else>{{ stat.number }}</span>
            </div>
            <div class="text-body-2 text-uppercase font-weight-medium stat-label">
              {{ stat.label }}
            </div>
          </div>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script setup lang="ts">
interface OverallStats {
  totalProjects: number
  totalCountries: number
}

const { t: $t } = useI18n()

// Load real stats
const overallStats = ref<OverallStats | null>(null)

onMounted(async () => {
  try {
    const response = await fetch('/data/overall-stats.json')
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
      number: '6',
      label: $t('stats.card3.label'),
      target: 6
    }
  ]
})

const isVisible = ref(false)
const animatedValues = ref(['0', '0', '0'])

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

  const section = document.querySelector('.stats-section')
  if (section) {
    observer.observe(section)
  }
})
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.stats-section {
  padding: $spacing-3xl 0;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
    top: -100%;
    left: -50%;
    animation: shimmer 15s ease-in-out infinite;
  }
}

.stat-card {
  text-align: center;
  padding: $spacing-lg;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: $border-radius-lg;
  border: 2px solid rgba(255, 255, 255, 0.2);
}

.stat-number {
  color: white;
  line-height: 1.2;
  margin-bottom: $spacing-sm;
}

.stat-label {
  color: rgba(255, 255, 255, 0.95);
  letter-spacing: 0.05em;
}
</style>
