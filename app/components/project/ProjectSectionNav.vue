<template>
  <nav v-if="sections.length >= 2" class="section-nav" aria-label="Project sections">
    <v-container class="section-nav-container">
      <ul>
        <li v-for="s in sections" :key="s.id">
          <a
            :href="`#${s.id}`"
            :class="{ active: activeId === s.id }"
            :aria-current="activeId === s.id ? 'location' : undefined"
            @click.prevent="navigate(s.id)"
          >
            {{ s.label }}
          </a>
        </li>
      </ul>
    </v-container>
  </nav>
</template>

<script setup lang="ts">
const props = defineProps<{
  sections: { id: string; label: string }[]
}>()

const activeId = ref<string | null>(null)
let observer: IntersectionObserver | null = null
let throttleTimer: ReturnType<typeof setTimeout> | null = null

const reducedMotion = () =>
  typeof window !== 'undefined' &&
  window.matchMedia('(prefers-reduced-motion: reduce)').matches

const navigate = (id: string) => {
  if (typeof window === 'undefined') return
  const el = document.getElementById(id)
  if (!el) return
  el.scrollIntoView({
    behavior: reducedMotion() ? 'auto' : 'smooth',
    block: 'start'
  })
  if (history.replaceState) history.replaceState(null, '', `#${id}`)
  activeId.value = id
}

const setupObserver = () => {
  if (typeof window === 'undefined' || typeof IntersectionObserver === 'undefined') return
  observer?.disconnect()
  observer = new IntersectionObserver(
    (entries) => {
      if (throttleTimer) return
      throttleTimer = setTimeout(() => {
        throttleTimer = null
        const visible = entries
          .filter((e) => e.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top)[0]
        if (visible?.target?.id) activeId.value = visible.target.id as string
      }, 100)
    },
    { rootMargin: '-30% 0% -50% 0%', threshold: 0 }
  )
  for (const s of props.sections) {
    const el = document.getElementById(s.id)
    if (el) observer.observe(el)
  }
}

const honorHashOnLoad = () => {
  if (typeof window === 'undefined') return
  const hash = window.location.hash?.slice(1)
  if (!hash) return
  if (!props.sections.some((s) => s.id === hash)) return
  requestAnimationFrame(() => {
    const el = document.getElementById(hash)
    if (el) {
      el.scrollIntoView({ behavior: 'auto', block: 'start' })
      activeId.value = hash
    }
  })
}

onMounted(() => {
  setupObserver()
  honorHashOnLoad()
})

watch(
  () => props.sections.map((s) => s.id).join(','),
  () => setupObserver()
)

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
  if (throttleTimer) {
    clearTimeout(throttleTimer)
    throttleTimer = null
  }
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section-nav {
  position: sticky;
  top: $sticky-site-header + $sticky-breadcrumb;
  z-index: 8;
  background: var(--page-bg, #f8f9fa);
  padding: $rhythm-2 0;
  border-bottom: 1px solid $border-soft;
  margin-bottom: $rhythm-4;

  /* Hidden on mobile — primary navigation on phone is scroll +
     the in-page section headings; the pill nav adds chrome without
     enough payoff at narrow widths. */
  @media (max-width: $detail-bp-tablet - 1) {
    display: none;
  }
}

.section-nav-container {
  max-width: $container-max-detail;

  ul {
    display: flex;
    gap: $rhythm-1;
    overflow-x: auto;
    scroll-behavior: smooth;
    -webkit-overflow-scrolling: touch;
    list-style: none;
    margin: 0;
    padding: 0;

    @media (max-width: $detail-bp-tablet - 1) {
      mask-image: linear-gradient(to right, black 90%, transparent);
    }
  }

  a {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.875rem;
    color: $text-caption;
    white-space: nowrap;
    text-decoration: none;
    transition:
      background 0.15s,
      color 0.15s;

    &:hover {
      background: rgba(0, 0, 0, 0.05);
      color: $text-primary;
    }

    &.active {
      background: $green-bright;
      color: white;
    }

    &:focus-visible {
      outline: 2px solid $green-dark;
      outline-offset: 2px;
    }
  }
}

@media (prefers-reduced-motion: reduce) {
  .section-nav-container ul {
    scroll-behavior: auto;
  }
}
</style>
