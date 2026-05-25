<template>
  <article class="team-card">
    <div v-if="resolvedPicture" class="team-picture">
      <nuxt-img :src="resolvedPicture" :alt="`${firstname} ${lastname}`" />
    </div>
    <div v-else :class="['team-avatar', { 'team-avatar-beige': beige }]">{{ initials }}</div>
    <div class="team-content">
      <div class="team-heading">
        <h3 class="team-name">{{ firstname }} {{ lastname }}</h3>
      </div>
      <p class="team-role">{{ role }}</p>
      <p v-if="details" class="team-bio">{{ details }}</p>
    </div>
  </article>
</template>

<script setup lang="ts">
const props = defineProps<{
  firstname: string
  lastname: string
  role: string
  details?: string
  beige?: boolean
  picture?: string
}>()

const { resolveImagePath } = useImagePath()

const initials = computed(() => {
  return (props.firstname.charAt(0) + props.lastname.charAt(0)).toUpperCase()
})

const resolvedPicture = computed(() => {
  return props.picture ? resolveImagePath(props.picture) : ''
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;
/* Sleek tile aesthetic at every viewport — no card frame, just a rounded
   photo + caption row with an arrow chip affordance. */
.team-card {
  background: transparent;
  border: none;
  overflow: visible;
  transition: transform 0.25s ease;

  &:hover {
    transform: translateY(-3px);

    .team-picture img {
      transform: scale(1.02);
    }
  }
}
.team-picture {
  aspect-ratio: 1;
  overflow: hidden;
  border-radius: 12px;
  background: $warm-beige;
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    transition: transform 0.4s ease;
  }
}
.team-avatar {
  aspect-ratio: 1;
  border-radius: 12px;
  background: $warm-beige;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: $font-family-base;
  font-size: 2.5rem;
  font-weight: 600;
  color: $forest-green;
}
.team-avatar-beige {
  background: #fff8e7;
}
.team-content {
  padding: 0.875rem 0.125rem 0;
}
.team-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.25rem;
}
.team-name {
  font-family: $font-family-base;
  font-size: 1.0625rem;
  font-weight: 600;
  margin: 0;
  line-height: 1.25;
  color: $brown-dark;
  flex: 1;
  min-width: 0;
  /* Cap to two lines so the row stays even across cards. */
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.team-role {
  font-size: 0.8125rem;
  font-weight: 500;
  color: $brown-dark;
  opacity: 0.75;
  margin: 0 0 0.25rem;
  line-height: 1.4;
}
.team-bio {
  font-size: 0.8125rem;
  line-height: 1.55;
  color: $brown-dark;
  opacity: 0.75;
  margin: 0.25rem 0 0;
}

/* Mobile fine-tunes: slightly smaller name + arrow to match the dense
   2-up grid without changing the structural pattern. */
@media (max-width: 600px) {
  .team-avatar {
    font-size: 2rem;
  }
  .team-content {
    padding: 0.625rem 0.125rem 0;
  }
  .team-heading {
    gap: 0.375rem;
    margin-bottom: 0.125rem;
  }
  .team-name {
    font-size: 0.9375rem;
  }
  .team-role {
    font-size: 0.75rem;
    line-height: 1.35;
  }
  .team-bio {
    font-size: 0.75rem;
    line-height: 1.5;
  }
}
</style>
