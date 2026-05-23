<template>
  <div>
    <TeamHero />

    <!-- Scientific Advisory Board -->
    <TeamSection
      v-if="scientificAdvisoryBoard.length"
      :title="$t('team.categories.scientificAdvisoryBoard.title')"
      :description="$t('team.categories.scientificAdvisoryBoard.description')"
    >
      <TeamMemberCard
        v-for="member in scientificAdvisoryBoard"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
      />
    </TeamSection>

    <!-- Principal Investigators -->
    <TeamSection
      v-if="principalInvestigators.length"
      :title="$t('team.categories.principalInvestigators.title')"
      :description="$t('team.categories.principalInvestigators.description')"
      beige
    >
      <TeamMemberCard
        v-for="member in principalInvestigators"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
        beige
      />
    </TeamSection>

    <!-- Co-Investigators & Post-Docs -->
    <TeamSection
      v-if="coInvestigators.length"
      :title="$t('team.categories.coInvestigators.title')"
      :description="$t('team.categories.coInvestigators.description')"
    >
      <TeamMemberCard
        v-for="member in coInvestigators"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
      />
    </TeamSection>

    <!-- Technology & AI Team -->
    <TeamSection
      v-if="technology.length"
      :title="$t('team.categories.technology.title')"
      :description="$t('team.categories.technology.description')"
      beige
    >
      <TeamMemberCard
        v-for="member in technology"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
        beige
      />
    </TeamSection>

    <!-- Project Management -->
    <TeamSection
      v-if="projectManagement.length"
      :title="$t('team.categories.projectManagement.title')"
      :description="$t('team.categories.projectManagement.description')"
    >
      <TeamMemberCard
        v-for="member in projectManagement"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
      />
    </TeamSection>

    <!-- Data & Fieldwork Team -->
    <TeamSection
      v-if="fieldwork.length"
      :title="$t('team.categories.fieldwork.title')"
      :description="$t('team.categories.fieldwork.description')"
      beige
    >
      <TeamMemberCard
        v-for="member in fieldwork"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
        beige
      />
    </TeamSection>

    <!-- Communication and Dissemination -->
    <TeamSection
      v-if="communicationDissemination.length"
      :title="$t('team.categories.communicationDissemination.title')"
      :description="$t('team.categories.communicationDissemination.description')"
    >
      <TeamMemberCard
        v-for="member in communicationDissemination"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
      />
    </TeamSection>

    <!-- Operations -->
    <TeamSection
      v-if="operations.length"
      :title="$t('team.categories.operations.title')"
      :description="$t('team.categories.operations.description')"
      beige
    >
      <TeamMemberCard
        v-for="member in operations"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
        beige
      />
    </TeamSection>

    <!-- Partner sections — Institutional · Design & Legal · Data Collection.
         Logo on top (real logo file → site favicon → monogram fallback), then
         the partner name, country and role below. -->
    <TeamSection
      v-for="(group, gi) in partnerGroups"
      :key="group.key"
      :title="$t(group.titleKey)"
      :description="$t(group.descKey)"
      :beige="gi % 2 === 1"
    >
      <component
        :is="partner.website ? 'a' : 'div'"
        v-for="partner in group.partners"
        :key="partner.name"
        class="partner-card"
        :href="partner.website || undefined"
        :target="partner.website ? '_blank' : undefined"
        :rel="partner.website ? 'noopener noreferrer' : undefined"
      >
        <div v-if="partnerLogo(partner)" class="partner-logo">
          <img
            :src="partnerLogo(partner)"
            :alt="partner.name"
            class="partner-logo-img"
            loading="lazy"
            @error="onLogoError(partner.name)"
          />
        </div>
        <div v-else class="partner-logo partner-logo--monogram" aria-hidden="true">
          {{ partnerMonogram(partner.name) }}
        </div>
        <div class="partner-content">
          <h3 class="partner-name">{{ partner.name }}</h3>
          <span v-if="partner.role" class="partner-role">{{ partner.role }}</span>
          <p class="partner-country">{{ partner.country }}</p>
        </div>
      </component>
    </TeamSection>

    <!-- Global Interviewer Network -->
    <TeamSection
      :title="$t('team.categories.globalInterviewerNetwork.title')"
      :description="$t('team.categories.globalInterviewerNetwork.description')"
      beige
    >
      <template #search>
        <div class="search-box">
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="$t('team.searchPlaceholder')"
            class="search-input"
          />
        </div>
      </template>
      <div
        v-for="interviewer in filteredGlobalInterviewers"
        :key="interviewer.name"
        class="interviewer-card"
      >
        <div v-if="getResolvedPicture(interviewer.picture)" class="interviewer-image-wrapper">
          <NuxtImg
            :src="getResolvedPicture(interviewer.picture)"
            :alt="interviewer.name"
            class="interviewer-image"
          />
        </div>
        <div v-else class="interviewer-avatar beige">{{ getInitials(interviewer.name) }}</div>
        <h3>{{ interviewer.name }}</h3>
        <p class="interviewer-country">{{ interviewer.country }}</p>
      </div>
    </TeamSection>
  </div>
</template>

<script setup lang="ts">
const { t: $t, locale } = useI18n()

useHead({
  title: $t('team.meta.title'),
  meta: [
    {
      name: 'description',
      content: $t('team.meta.description')
    }
  ]
})

const { resolveImagePath } = useImagePath()

const { data: allTeamMembers } = await useAsyncData(`all-team-members-${locale.value}`, () =>
  queryCollection('team').where('path', 'LIKE', `/team/${locale.value}/%`).all(),
  { default: () => [] }
)

const principalInvestigators = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'principal-investigators') || []
})

const coInvestigators = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'co-investigators') || []
})

const technology = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'technology') || []
})

const projectManagement = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'project-management') || []
})

const fieldwork = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'fieldwork') || []
})

const operations = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'operations') || []
})

const scientificAdvisoryBoard = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'scientific-advisory-board') || []
})

const communicationDissemination = computed(() => {
  return allTeamMembers.value?.filter((m: any) => m.category === 'communication-dissemination') || []
})

const { data: allPartners } = await useAsyncData(`all-partners-${locale.value}`, () =>
  queryCollection('partners').where('path', 'LIKE', `/partners/${locale.value}/%`).all(),
  { default: () => [] }
)

const institutionalPartners = computed(() =>
  (allPartners.value || []).find(
    (p: any) => p.category === 'institutional-partners' && p.partners && Array.isArray(p.partners)
  ) ?? null
)

const designLegalPartners = computed(() =>
  (allPartners.value || []).find(
    (p: any) => p.category === 'design-legal-partners' && p.partners && Array.isArray(p.partners)
  ) ?? null
)

const dataCollectionPartners = computed(() =>
  (allPartners.value || []).find(
    (p: any) => p.category === 'data-collection-partners' && p.partners && Array.isArray(p.partners)
  ) ?? null
)

// The three partner sections, in display order. Empty groups are dropped so
// the beige/cream alternation (gi % 2) stays predictable.
const partnerGroups = computed(() =>
  [
    {
      key: 'institutional',
      titleKey: 'team.categories.institutionalPartners.title',
      descKey: 'team.categories.institutionalPartners.description',
      partners: institutionalPartners.value?.partners
    },
    {
      key: 'design-legal',
      titleKey: 'team.categories.designLegalPartners.title',
      descKey: 'team.categories.designLegalPartners.description',
      partners: designLegalPartners.value?.partners
    },
    {
      key: 'data-collection',
      titleKey: 'team.categories.dataCollectionPartners.title',
      descKey: 'team.categories.dataCollectionPartners.description',
      partners: dataCollectionPartners.value?.partners
    }
  ]
    .filter((g) => Array.isArray(g.partners) && g.partners.length > 0)
    .map((g) => ({ ...g, partners: g.partners as any[] }))
)

// Partner logo, best → fallback:
//   0. the `logo:` from the entry — either a local file in /public or an
//      absolute URL to the org's own logo (set per-partner where we could find
//      one); failing that, the largest icon icon.horse has for the domain
//   1. the Google favicon for that domain (lower res, always available)
//   2. nothing → the component shows a monogram instead
// A couple of domains only return a generic placeholder from icon.horse and
// have no logo on file — denylist those so they go straight to a clean
// monogram. `logoStage` bumps a card down a step on image error.
const LOGO_DENYLIST = new Set(['habitusinsight.com', 'hijink.co', '1labconsulting.com'])
const logoStage = reactive<Record<string, number>>({})
const onLogoError = (name: string) => {
  logoStage[name] = (logoStage[name] ?? 0) + 1
}

const resolveLogo = (logo: string): string =>
  /^https?:\/\//i.test(logo) ? logo : resolveImagePath(logo)

const partnerLogo = (p: { name: string; logo?: string; website?: string }): string => {
  const stage = logoStage[p.name] ?? 0
  if (p.logo) return stage === 0 ? resolveLogo(p.logo) : ''
  if (!p.website) return ''
  let host: string
  try {
    host = new URL(p.website).hostname.replace(/^www\./, '')
  } catch {
    return ''
  }
  if (LOGO_DENYLIST.has(host)) return ''
  if (stage === 0) return `https://icon.horse/icon/${host}`
  if (stage === 1) return `https://www.google.com/s2/favicons?domain=${host}&sz=256`
  return ''
}

const partnerMonogram = (name: string): string => {
  const acronym = name.match(/\(([A-Za-z0-9][A-Za-z0-9.\-&]{1,7})\)/)
  if (acronym) return acronym[1].replace(/[^A-Za-z0-9]/g, '').toUpperCase().slice(0, 5)
  const stop = new Set([
    'the', 'of', 'and', 'de', 'in', 'a', 'an', 'for',
    'ltd', 'inc', 'llc', 'co', 'gmbh', 'sas'
  ])
  const words = name
    .replace(/[(),]/g, ' ')
    .split(/\s+/)
    .filter((w) => w && !stop.has(w.toLowerCase()))
  if (!words.length) return name.replace(/[^A-Za-z0-9]/g, '').slice(0, 2).toUpperCase() || '•'
  const first = words[0]!
  if (/[A-Z]/.test(first) && /^[A-Z0-9][A-Z0-9.\-&]+$/.test(first)) {
    return first.replace(/[^A-Za-z0-9]/g, '').toUpperCase().slice(0, 4)
  }
  if (words.length === 1) return first.toUpperCase().slice(0, 2)
  return (first[0]! + words[1]![0]!).toUpperCase()
}

const { data: allInterviewers } = await useAsyncData('all-interviewers', () =>
  queryCollection('interviewers').all(),
  { default: () => [] }
)

const globalNetwork = computed(() => {
  if (!allInterviewers.value) return null
  return allInterviewers.value.find((i: any) => i.category === 'global-interviewer-network')
})

const searchQuery = ref('')

const getInitials = (name: string) => {
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0].charAt(0) + parts[parts.length - 1].charAt(0)).toUpperCase()
  }
  return name.charAt(0).toUpperCase()
}

const getResolvedPicture = (picture: string) => {
  return picture ? resolveImagePath(picture) : ''
}

const filteredGlobalInterviewers = computed(() => {
  if (!globalNetwork.value?.interviewers) return []
  if (!searchQuery.value) return globalNetwork.value.interviewers
  const query = searchQuery.value.toLowerCase()
  return globalNetwork.value.interviewers.filter(
    (interviewer: any) =>
      interviewer.name.toLowerCase().includes(query) ||
      interviewer.country.toLowerCase().includes(query)
  )
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

/* No card frame — just the logo, then the name, tag and location stacked
   beneath it. The whole thing links to the partner's site when one is on file. */
.partner-card {
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  transition: transform 0.25s ease;

  &:hover {
    transform: translateY(-3px);
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 4px;
  }
}

/* The logo only — no box, border, background or padding. It's sized to fill a
   square slot so the cards line up, with object-fit keeping it undistorted. */
.partner-logo {
  display: flex;
  align-items: center;
  justify-content: center;
  aspect-ratio: 1;
}

.partner-logo-img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.partner-logo--monogram {
  color: $green-forest;
  font-family: $font-family-display;
  font-size: clamp(2rem, 5vw, 2.75rem);
  font-weight: 700;
  letter-spacing: 0.03em;
}

.partner-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.4rem;
  padding: 0.875rem 0.25rem 0;
}

.partner-name {
  margin: 0;
  font-family: $font-family-base;
  font-size: 1.0625rem;
  font-weight: 600;
  line-height: 1.3;
  color: $brown-dark;
}

.interviewer-card {
  background: white;
  padding: 1.5rem;
  border: 2px solid $warm-beige;
  transition: all 0.3s ease;
  text-align: center;

  &:hover {
    transform: translateY(-3px);
    border-color: $green-bright;
    box-shadow: 0 8px 24px rgba(44, 36, 22, 0.1);
  }

  h3 {
    color: $brown-dark;
    font-size: 1rem;
    margin-bottom: 0.25rem;
    font-weight: 600;
  }
}

.interviewer-image-wrapper {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 auto 1rem;
  border: 2px solid $warm-beige;
}

.interviewer-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.interviewer-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: $warm-beige;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 600;
  color: $forest-green;
  margin: 0 auto 1rem;

  &.beige {
    background: $cream;
  }
}

.partner-country {
  margin: 0;
  font-size: 0.8125rem;
  line-height: 1.4;
  color: $brown-dark;
  opacity: 0.7;
}

.interviewer-country {
  color: $green-bright;
  font-size: 0.85rem;
}

.partner-role {
  display: inline-block;
  padding: 3px 9px;
  border-radius: 999px;
  background: rgba(76, 160, 73, 0.1);
  color: $green-forest;
  font-family: $font-family-base;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.search-box {
  width: 100%;
  max-width: 600px;
  margin: 0 auto 3rem;
}

.search-input {
  width: 100%;
  padding: 1rem 1.5rem;
  border: 2px solid $brown-dark;
  border-radius: 0;
  background: white;
  font-size: 1rem;
  font-family: $font-family-base;
  transition: border-color 0.3s;

  &:focus {
    outline: none;
    border-color: $green-bright;
  }

  &::placeholder {
    color: #999;
  }
}
</style>
