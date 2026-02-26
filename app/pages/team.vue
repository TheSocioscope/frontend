<template>
  <div>
    <TeamHero />

    <!-- Principal Investigators -->
    <TeamSection
      v-if="principalInvestigators.length"
      :title="$t('team.categories.principalInvestigators.title')"
      :description="$t('team.categories.principalInvestigators.description')"
    >
      <TeamMemberCard
        v-for="member in principalInvestigators"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
      />
    </TeamSection>

    <!-- Co-Investigators & Post-Docs -->
    <TeamSection
      v-if="coInvestigators.length"
      :title="$t('team.categories.coInvestigators.title')"
      :description="$t('team.categories.coInvestigators.description')"
      beige
    >
      <TeamMemberCard
        v-for="member in coInvestigators"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
        beige
      />
    </TeamSection>

    <!-- Technology & AI Team -->
    <TeamSection
      v-if="technology.length"
      :title="$t('team.categories.technology.title')"
      :description="$t('team.categories.technology.description')"
    >
      <TeamMemberCard
        v-for="member in technology"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
      />
    </TeamSection>

    <!-- Project Management -->
    <TeamSection
      v-if="projectManagement.length"
      :title="$t('team.categories.projectManagement.title')"
      :description="$t('team.categories.projectManagement.description')"
      beige
    >
      <TeamMemberCard
        v-for="member in projectManagement"
        :key="member._path"
        :firstname="member.firstname"
        :lastname="member.lastname"
        :role="member.role"
        :details="member.details"
        :picture="member.picture"
        beige
      />
    </TeamSection>

    <!-- Data & Fieldwork Team -->
    <TeamSection
      v-if="fieldwork.length"
      :title="$t('team.categories.fieldwork.title')"
      :description="$t('team.categories.fieldwork.description')"
    >
      <TeamMemberCard
        v-for="member in fieldwork"
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

    <!-- Institutional Partners -->
    <TeamSection
      v-if="institutionalPartners"
      :title="$t('team.categories.institutionalPartners.title')"
      :description="$t('team.categories.institutionalPartners.description')"
    >
      <div
        v-for="partner in institutionalPartners?.partners || []"
        :key="partner.name"
        class="partner-card"
      >
        <h3>{{ partner.name }}</h3>
        <p class="partner-country">{{ partner.country }}</p>
        <p class="partner-role">{{ partner.role }}</p>
      </div>
    </TeamSection>

    <!-- Design and Legal Partners -->
    <TeamSection
      v-if="designLegalPartners"
      :title="$t('team.categories.designLegalPartners.title')"
      :description="$t('team.categories.designLegalPartners.description')"
      beige
    >
      <div
        v-for="partner in designLegalPartners?.partners || []"
        :key="partner.name"
        class="partner-card"
      >
        <h3>{{ partner.name }}</h3>
        <p class="partner-country">{{ partner.country }}</p>
        <p class="partner-role">{{ partner.role }}</p>
      </div>
    </TeamSection>

    <!-- Data Collection Partners -->
    <TeamSection
      v-if="dataCollectionPartners"
      :title="$t('team.categories.dataCollectionPartners.title')"
      :description="$t('team.categories.dataCollectionPartners.description')"
    >
      <div
        v-for="partner in dataCollectionPartners?.partners || []"
        :key="partner.name"
        class="partner-card"
      >
        <h3>{{ partner.name }}</h3>
        <p class="partner-country">{{ partner.country }}</p>
        <p class="partner-role">{{ partner.role }}</p>
      </div>
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

const { data: allTeamMembers } = await useAsyncData('all-team-members', () =>
  queryCollection('team').all(),
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

const { data: allPartners } = await useAsyncData('all-partners', () =>
  queryCollection('partners').all(),
  { default: () => [] }
)

const institutionalPartners = computed(() => {
  if (!allPartners.value) return null
  return allPartners.value.find(
    (p: any) => p.category === 'institutional-partners' && p.partners && Array.isArray(p.partners)
  )
})

const designLegalPartners = computed(() => {
  if (!allPartners.value) return null
  return allPartners.value.find(
    (p: any) => p.category === 'design-legal-partners' && p.partners && Array.isArray(p.partners)
  )
})

const dataCollectionPartners = computed(() => {
  if (!allPartners.value) return null
  return allPartners.value.find(
    (p: any) => p.category === 'data-collection-partners' && p.partners && Array.isArray(p.partners)
  )
})

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

.partner-card {
  background: white;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  h3 {
    color: $brown-dark;
    font-size: 1.25rem;
    margin-bottom: 0.75rem;
    font-weight: 600;
  }
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
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
}

.interviewer-country {
  color: $green-bright;
  font-size: 0.85rem;
}

.partner-role {
  color: $green-bright;
  font-weight: 600;
  font-size: 1rem;
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
  font-family: 'Playfair Display', serif;
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
