<template>
  <v-card v-if="project.team && project.team.length > 0" id="team" class="project-team">
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-account-group-outline</v-icon>
      {{ $t('common.team') }}
    </v-card-title>
    <v-card-text>
      <v-row>
        <v-col v-for="(member, index) in project.team" :key="index" cols="12" sm="6" md="4" lg="3">
          <v-card class="team-card" elevation="2">
            <div class="team-avatar-container">
              <v-avatar
                :image="member.photo"
                :alt="`${member.firstname} ${member.lastname}`"
                size="120"
                class="team-avatar"
              >
                <v-icon v-if="!member.photo" size="60">mdi-account</v-icon>
              </v-avatar>
            </div>

            <v-card-title class="team-name">
              {{ member.firstname }} {{ member.lastname }}
            </v-card-title>

            <v-card-subtitle v-if="member.role" class="team-role">
              {{ member.role }}
            </v-card-subtitle>

            <v-card-text v-if="member.bio" class="team-bio">
              {{ member.bio }}
            </v-card-text>

            <v-card-actions v-if="member.url || member.email" class="team-actions">
              <v-btn
                v-if="member.url"
                :href="member.url"
                target="_blank"
                icon
                size="small"
                variant="text"
              >
                <v-icon>mdi-web</v-icon>
              </v-btn>

              <v-btn
                v-if="member.email"
                :href="`mailto:${member.email}`"
                icon
                size="small"
                variant="text"
              >
                <v-icon>mdi-email</v-icon>
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  project: any
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
.project-team {
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
}

.team-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.5rem 1rem;
  transition:
    transform 0.2s ease,
    box-shadow 0.2s ease;

  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15) !important;
  }
}

.team-avatar-container {
  margin-bottom: 1rem;
}

.team-avatar {
  border: 3px solid rgb(var(--v-theme-primary));
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.team-name {
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.3;
  padding: 0.5rem 1rem;
  word-break: break-word;
}

.team-role {
  font-size: 0.95rem;
  color: rgba(0, 0, 0, 0.6);
  font-style: italic;
  padding: 0 1rem 0.5rem;
}

.team-bio {
  font-size: 0.9rem;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.7);
  flex-grow: 1;
}

.team-actions {
  justify-content: center;
  padding-top: 0.5rem;
}
</style>
