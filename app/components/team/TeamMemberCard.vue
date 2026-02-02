<template>
  <div class="team-card">
    <div v-if="resolvedPicture" class="team-picture">
      <nuxt-img :src="resolvedPicture" :alt="`${firstname} ${lastname}`" />
    </div>
    <div v-else :class="['team-avatar', { 'team-avatar-beige': beige }]">{{ initials }}</div>
    <div class="team-content">
      <h3 class="team-name">{{ firstname }} {{ lastname }}</h3>
      <p class="team-role">{{ role }}</p>
      <p v-if="details" class="team-bio">{{ details }}</p>
    </div>
  </div>
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

.team-card {
  background: white;
  border: 2px solid $warm-beige;
  overflow: hidden;
  transition: all 0.4s ease;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 36px rgba(44, 36, 22, 0.15);
    border-color: $green-bright;
  }
}

.team-picture {
  aspect-ratio: 1;
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
  }
}

.team-avatar {
  aspect-ratio: 1;
  background: $warm-beige;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Playfair Display', serif;
  font-size: 3rem;
  font-weight: 600;
  color: $forest-green;
}
.team-avatar-beige {
  background: #fff8e7;
}
.team-content {
  padding: 1.5rem;
}

.team-name {
  font-family: 'Playfair Display', serif;
  font-size: 1.25rem;
  margin-bottom: 0.35rem;
  font-weight: 700;
}

.team-role {
  color: $green-bright;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  font-weight: 600;
}

.team-bio {
  font-size: 0.9rem;
  opacity: 0.8;
  line-height: 1.6;
  margin: 0;
}
</style>
