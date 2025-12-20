<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" class="text-center mb-8">
        <h1 class="text-h2 mb-4">{{ $t('team.title') }}</h1>
        <p class="text-h6">{{ $t('team.subtitle') }}</p>
      </v-col>
    </v-row>

    <!-- Leadership -->
    <v-row justify="center" class="mb-12">
      <v-col cols="12" class="text-center mb-6">
        <h2 class="text-h3">{{ $t('team.leadership.title') }}</h2>
      </v-col>
      <v-col v-for="(member, i) in leadership" :key="i" cols="12" sm="6" md="4">
        <v-card class="team-card" elevation="0">
          <v-card-text class="text-center">
            <div class="team-photo mb-4">{{ member.initial }}</div>
            <h3 class="mb-2">{{ $t(member.name) }}</h3>
            <p class="role mb-2">{{ $t(member.role) }}</p>
            <p class="organization">{{ $t(member.org) }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Researchers -->
    <section class="section-beige py-12">
      <v-container>
        <v-row>
          <v-col cols="12" class="text-center mb-6">
            <h2 class="text-h3">{{ $t('team.researchers.title') }}</h2>
          </v-col>
          <v-col v-for="(member, i) in researchers" :key="i" cols="12" sm="6" md="3">
            <v-card class="team-card" elevation="0">
              <v-card-text class="text-center">
                <div class="team-photo mb-4">{{ member.initial }}</div>
                <h4 class="mb-2">{{ $t(member.name) }}</h4>
                <p class="role">{{ $t(member.role) }}</p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>
  </v-container>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: t('team.title')
})

const leadership = [
  { name: 'team.helga.name', role: 'team.helga.role', org: 'team.helga.org', initial: 'HN' },
  { name: 'team.saadi.name', role: 'team.saadi.role', org: 'team.saadi.org', initial: 'SL' }
]

const researchers = [
  { name: 'team.researcher1.name', role: 'team.researcher1.role', initial: 'RC' },
  { name: 'team.researcher2.name', role: 'team.researcher2.role', initial: 'DA' },
  { name: 'team.researcher3.name', role: 'team.researcher3.role', initial: 'FR' },
  { name: 'team.researcher4.name', role: 'team.researcher4.role', initial: 'TL' }
]
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.team-photo {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: $green-bright;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  font-weight: 600;
  margin: 0 auto;
}

.role {
  color: $green-bright;
  font-weight: 600;
}

.organization {
  opacity: 0.7;
  font-size: 0.95rem;
}
</style>
