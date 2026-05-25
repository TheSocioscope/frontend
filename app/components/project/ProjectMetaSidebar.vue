<template>
  <aside class="project-meta-sidebar" aria-label="Initiative metadata">
    <details ref="detailsEl" :open="isDesktop" class="sidebar-details">
      <summary class="sidebar-summary">
        <v-icon size="small">mdi-information-outline</v-icon>
        <span>{{ localizedName }}</span>
        <v-icon class="chevron" size="small">mdi-chevron-down</v-icon>
      </summary>

      <div class="sidebar-body">
        <div class="logo-wrap">
          <div class="logo">
            <v-img
              v-if="project.logo"
              :src="resolveImagePath(project.logo)"
              :alt="localizedName"
              cover
            />
            <div v-else class="logo-placeholder">🌱</div>
          </div>
        </div>

        <dl v-if="factRows.length" class="key-facts">
          <template v-for="row in factRows" :key="row.label">
            <dt>{{ row.label }}</dt>
            <dd>{{ row.value }}</dd>
          </template>
        </dl>

        <div class="cta-stack">
          <v-btn
            color="success"
            size="large"
            block
            prepend-icon="mdi-account-plus-outline"
            @click="emit('connect')"
          >
            {{ $t('common.connectButton') }}
          </v-btn>

          <v-btn
            v-if="project.url"
            :href="project.url"
            target="_blank"
            rel="noopener noreferrer"
            color="primary"
            variant="outlined"
            size="large"
            block
            append-icon="mdi-open-in-new"
          >
            {{ $t('products.visitWebsite') }}
          </v-btn>

          <v-btn
            variant="text"
            size="small"
            block
            prepend-icon="mdi-pencil"
            @click="emit('edit')"
          >
            {{ $t('editDrawer.title') }}
          </v-btn>
        </div>

        <div class="share-strip">
          <span class="share-label">{{ $t('projects.detail.share') }}</span>
          <div class="share-icons">
            <a
              :href="facebookShareUrl"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="Facebook"
            >
              <v-icon>mdi-facebook</v-icon>
            </a>
            <a
              :href="linkedinShareUrl"
              target="_blank"
              rel="noopener noreferrer"
              aria-label="LinkedIn"
            >
              <v-icon>mdi-linkedin</v-icon>
            </a>
            <a :href="emailShareUrl" aria-label="Email">
              <v-icon>mdi-email</v-icon>
            </a>
            <button
              type="button"
              class="copy-btn"
              :aria-label="$t('common.copyLink')"
              @click="copyLink"
            >
              <v-icon>{{ copied ? 'mdi-check' : 'mdi-content-copy' }}</v-icon>
            </button>
          </div>
        </div>
      </div>
    </details>
  </aside>
</template>

<script setup lang="ts">
const props = defineProps<{
  project: any
  localizedName: string
  pageUrl: string
}>()

const emit = defineEmits<{
  connect: []
  edit: []
}>()

const { t: $t } = useI18n()
const { resolveImagePath } = useImagePath()
const { getContinentLabel, getCountryLabel, getStatusLabel } = useProjectMappings()

const isDesktop = ref(true)
let mql: MediaQueryList | null = null

const updateIsDesktop = (e: MediaQueryListEvent | MediaQueryList) => {
  isDesktop.value = e.matches
}

onMounted(() => {
  if (typeof window === 'undefined') return
  mql = window.matchMedia('(min-width: 1024px)')
  isDesktop.value = mql.matches
  mql.addEventListener('change', updateIsDesktop)
})

onBeforeUnmount(() => {
  mql?.removeEventListener('change', updateIsDesktop)
})

const joinList = (val: unknown, mapper?: (v: string) => string) => {
  if (!val) return ''
  const arr = Array.isArray(val) ? val : [val]
  return arr.filter(Boolean).map((v) => (mapper ? mapper(String(v)) : String(v))).join(', ')
}

const factRows = computed(() => {
  const p = props.project ?? {}
  const rows: { label: string; value: string }[] = []

  const continents = joinList(p.continent, getContinentLabel)
  if (continents) rows.push({ label: 'Continent', value: continents })

  const countries = joinList(p.country, getCountryLabel)
  if (countries) rows.push({ label: 'Country', value: countries })

  const sectors = joinList(p.sectorFocus)
  if (sectors) rows.push({ label: 'Sector', value: sectors })

  const roles = joinList(p.entityRole)
  if (roles) rows.push({ label: 'Role', value: roles })

  if (p.entitySize) rows.push({ label: 'Size', value: String(p.entitySize) })
  if (p.geoReach) rows.push({ label: 'Geo reach', value: String(p.geoReach) })
  if (p.bizModel) rows.push({ label: 'Business model', value: String(p.bizModel) })
  if (p.resourceType) rows.push({ label: 'Resource', value: String(p.resourceType) })

  if (p.status !== undefined && p.status !== null && p.status !== '') {
    const statusVal = typeof p.status === 'string' ? getStatusLabel(p.status) : String(p.status)
    rows.push({ label: 'Status', value: statusVal })
  }

  return rows
})

const encodedUrl = computed(() => encodeURIComponent(props.pageUrl || ''))
const encodedTitle = computed(() => encodeURIComponent(props.localizedName || ''))

const facebookShareUrl = computed(
  () => `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl.value}`
)
const linkedinShareUrl = computed(
  () => `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl.value}`
)
const emailShareUrl = computed(
  () => `mailto:?subject=${encodedTitle.value}&body=${encodedUrl.value}`
)

const copied = ref(false)
const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(props.pageUrl || window.location.href)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-meta-sidebar {
  width: 100%;

  @media (min-width: $detail-bp-desktop) {
    position: sticky;
    top: $sticky-sidebar-top;
    align-self: start; // critical: makes sticky engage inside CSS grid
    max-height: calc(100vh - #{$sticky-sidebar-top} - #{$rhythm-3});
    overflow-y: auto;
  }
}

.sidebar-details {
  background: white;
  border: 1px solid $border-soft;
  border-radius: 12px;
  padding: $rhythm-3;
}

.sidebar-summary {
  display: flex;
  align-items: center;
  gap: $rhythm-1;
  font-weight: 600;
  cursor: pointer;
  list-style: none;
  color: $green-dark;

  &::-webkit-details-marker {
    display: none;
  }

  span {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .chevron {
    transition: transform 0.2s;
  }
}

.sidebar-details[open] .sidebar-summary .chevron {
  transform: rotate(180deg);
}

@media (min-width: $detail-bp-desktop) {
  .sidebar-summary {
    display: none;
  }

  .sidebar-details {
    padding: $rhythm-3;
  }
}

.sidebar-body {
  display: flex;
  flex-direction: column;
  gap: $rhythm-3;
  padding-top: $rhythm-3;
}

@media (min-width: $detail-bp-desktop) {
  .sidebar-body {
    padding-top: 0;
  }
}

.logo-wrap {
  display: flex;
  justify-content: flex-start;
}

.logo {
  width: $logo-desktop;
  height: $logo-desktop;
  background-color: $surface-cream;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid $green-bright;
  overflow: hidden;
  flex-shrink: 0;
}

.logo-placeholder {
  font-size: 32px;
}

.key-facts {
  display: grid;
  grid-template-columns: 38% 62%;
  row-gap: $rhythm-1;
  column-gap: $rhythm-2;
  margin: 0;

  dt {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: $text-caption;
    align-self: center;
    margin: 0;
  }

  dd {
    margin: 0;
    font-size: 14px;
    color: $text-primary;
    line-height: 1.4;
  }
}

.cta-stack {
  display: flex;
  flex-direction: column;
  gap: $rhythm-1;

  /* On mobile the action bar at the top + sticky CTA at the bottom
     already cover Connect, Website, and Edit. Hiding the duplicates
     in the sidebar keeps the surface to one source of truth. */
  @media (max-width: $detail-bp-desktop - 1) {
    display: none;
  }
}

/* The sidebar logo is purely decorative on mobile (no key-fact value)
   — drop it on phones to recover ~120px and let key facts breathe. */
@media (max-width: $detail-bp-desktop - 1) {
  .logo-wrap {
    display: none;
  }
}

.share-strip {
  border-top: 1px solid $border-soft;
  padding-top: $rhythm-2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: $rhythm-2;
}

.share-label {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: $text-caption;
}

.share-icons {
  display: flex;
  gap: $rhythm-1;

  a,
  .copy-btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    border-radius: 50%;
    color: $text-caption;
    background: transparent;
    border: none;
    cursor: pointer;
    text-decoration: none;
    transition: background 0.15s;

    &:hover {
      background: rgba(0, 0, 0, 0.06);
      color: $green-dark;
    }

    &:focus-visible {
      outline: 2px solid $green-dark;
      outline-offset: 2px;
    }
  }
}
</style>
