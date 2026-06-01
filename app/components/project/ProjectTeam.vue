<template>
  <section v-if="project.team && project.team.length > 0" id="team" class="project-team">
    <span class="section-label">{{ $t('projects.detail.team') }}</span>

    <ul class="team-grid">
      <li
        v-for="(member, index) in project.team"
        :key="index"
        class="team-card"
      >
        <div class="team-avatar-wrap">
          <img
            v-if="member.photo"
            :src="member.photo"
            :alt="fullName(member)"
            class="team-avatar"
          />
          <div v-else class="team-avatar team-avatar-fallback">
            <v-icon size="32">mdi-account</v-icon>
          </div>
        </div>

        <div class="team-text">
          <h3 class="team-name">{{ fullName(member) }}</h3>
          <p v-if="member.role" class="team-role">{{ member.role }}</p>
          <p v-if="member.bio" class="team-bio">{{ member.bio }}</p>
        </div>

        <div v-if="member.url || member.email" class="team-actions">
          <a
            v-if="member.url"
            :href="member.url"
            target="_blank"
            rel="noopener noreferrer"
            class="team-action"
            :aria-label="`${fullName(member)} — website`"
          >
            <v-icon size="small">mdi-web</v-icon>
          </a>
          <a
            v-if="member.email"
            :href="`mailto:${member.email}`"
            class="team-action"
            :aria-label="`${fullName(member)} — email`"
          >
            <v-icon size="small">mdi-email-outline</v-icon>
          </a>
        </div>
      </li>
    </ul>
  </section>
</template>

<script setup lang="ts">
defineProps<{
  project: any
}>()

const { t: $t } = useI18n()

const fullName = (member: any): string => {
  const parts = [member.firstname, member.lastname].filter(Boolean)
  return parts.join(' ').trim() || member.name || ''
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section-label {
  display: block;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: $text-secondary;
  margin-bottom: $rhythm-2;
}

.project-team {
  margin-bottom: $rhythm-6;
  scroll-margin-top: $sticky-site-header + $sticky-breadcrumb + $rhythm-2;

  @media (max-width: $detail-bp-tablet - 1) {
    margin-bottom: $rhythm-3;
  }
}

.team-grid {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  /* 4-col desktop, 3-col tablet, 2-col mobile, 1-col on tiny phones */
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: $rhythm-3;

  @media (max-width: 1280px) {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  @media (max-width: $detail-bp-tablet - 1) {
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  @media (max-width: 380px) {
    grid-template-columns: 1fr;
  }
}

.team-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  background: white;
  border: 1px solid $border-soft;
  border-radius: 10px;
  padding: $rhythm-3 $rhythm-2 $rhythm-2;
  transition:
    border-color 0.15s,
    transform 0.15s,
    box-shadow 0.15s;

  &:hover {
    border-color: $green-leaf;
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.05);
  }

  @media (max-width: $detail-bp-tablet - 1) {
    padding: $rhythm-2 12px;
    border-radius: 8px;

    &:hover {
      transform: none;
      box-shadow: none;
    }
  }
}

.team-avatar-wrap {
  margin-bottom: $rhythm-2;
}

.team-avatar {
  display: block;
  width: 88px;
  height: 88px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid $earth-15;
  background: $earth-5;

  @media (max-width: $detail-bp-tablet - 1) {
    width: 64px;
    height: 64px;
  }
}

.team-avatar-fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  color: $earth-50;
}

.team-text {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 0;
  width: 100%;
}

.team-name {
  margin: 0;
  font-family: $font-family-display;
  font-size: 1rem;
  font-weight: 700;
  line-height: 1.25;
  color: $text-primary;
  /* 2-line clamp keeps cards uniform when names wrap */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 0.9375rem;
  }
}

.team-role {
  margin: 0;
  font-size: 0.8125rem;
  font-weight: 500;
  color: $green-forest;
  line-height: 1.3;
  /* Single line + ellipsis for the role */
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 0.75rem;
  }
}

.team-bio {
  margin: 4px 0 0;
  font-size: 0.8125rem;
  line-height: 1.5;
  color: $text-secondary;
  /* 3-line clamp on desktop, 2-line on mobile */
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;

  @media (max-width: $detail-bp-tablet - 1) {
    font-size: 0.75rem;
    line-height: 1.4;
    -webkit-line-clamp: 2;
    line-clamp: 2;
  }
}

.team-actions {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  margin-top: 10px;
}

.team-action {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: $text-caption;
  background: transparent;
  text-decoration: none;
  transition:
    color 0.15s,
    background 0.15s;

  &:hover {
    color: $green-forest;
    background: $earth-10;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }

  @media (max-width: $detail-bp-tablet - 1) {
    width: 28px;
    height: 28px;
  }
}
</style>
