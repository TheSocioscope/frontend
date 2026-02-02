<template>
  <div>
    <!-- Card with YouTube thumbnail -->
    <v-card
      v-if="project.yt && thumbnailUrl"
      class="project-card project-card-video"
      hover
      @click="handleClick"
    >
      <!-- Background Image (YouTube thumbnail) -->
      <div
        class="project-card-bg"
        :style="{
          backgroundImage: `url(${thumbnailUrl})`,
          backgroundSize: 'cover',
          backgroundPosition: 'center'
        }"
      />

      <!-- Content overlay - visible on hover -->
      <div class="project-card-overlay">
        <div class="overlay-content">
          <h3 class="text-h6 mb-3 font-weight-bold text-white">{{ localizedName }}</h3>
          <v-chip
            v-if="project.status !== undefined"
            size="small"
            class="mb-2"
            :color="getStatusColor(project.status)"
          >
            {{ getStatusLabel(project.status) }}
          </v-chip>
          <p v-if="project.location" class="text-caption mb-2 text-white">
            <v-icon size="x-small" class="mr-1">mdi-map-marker</v-icon>
            {{ project.location }}
          </p>
          <p class="text-body-2 mb-3 text-white" :class="descriptionClampClass">
            {{ localizedDescription }}
          </p>
          <div class="chip-container">
            <v-chip
              v-for="continentId in project.continent?.slice(0, 3) || []"
              :key="continentId"
              size="x-small"
              variant="outlined"
              color="white"
              class="mr-1 mb-1"
            >
              {{ getContinentLabel(continentId) }}
            </v-chip>
            <v-chip
              v-if="(project.continent?.length || 0) > 3"
              size="x-small"
              variant="outlined"
              color="white"
              class="mb-1"
            >
              +{{ (project.continent?.length || 0) - 3 }}
            </v-chip>
          </div>
        </div>
      </div>
    </v-card>

    <!-- Card without YouTube (traditional style) -->
    <v-card v-else class="project-card project-card-traditional" hover @click="handleClick">
      <div class="traditional-content">
        <div class="traditional-top">
          <v-chip
            v-if="project.status !== undefined"
            size="small"
            class="mb-2"
            :color="getStatusColor(project.status)"
          >
            {{ getStatusLabel(project.status) }}
          </v-chip>
        </div>
        <div class="traditional-middle">
          <h3 class="text-h6 mb-3 font-weight-bold text-grey-darken-4">{{ localizedName }}</h3>
          <p v-if="project.location" class="text-caption mb-2 text-grey-darken-2">
            <v-icon size="x-small" class="mr-1">mdi-map-marker</v-icon>
            {{ project.location }}
          </p>
          <p class="text-body-2 text-grey-darken-3" :class="descriptionClampClass">
            {{ localizedDescription }}
          </p>
        </div>
        <div class="traditional-bottom">
          <v-chip
            v-for="continentId in project.continent?.slice(0, 3) || []"
            :key="continentId"
            size="x-small"
            class="mr-1 mb-1"
          >
            {{ getContinentLabel(continentId) }}
          </v-chip>
          <v-chip v-if="(project.continent?.length || 0) > 3" size="x-small" class="mb-1">
            +{{ (project.continent?.length || 0) - 3 }}
          </v-chip>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script setup lang="ts">
interface Project {
  yt?: string
  status?: string
  location?: string
  description?: string | Record<string, string>
  continent?: string[]
  name: string | Record<string, string>
  pubId: number
  stem: string
  originalLang?: string
}

interface Props {
  project: Project
}

const props = defineProps<Props>()

const emit = defineEmits<{
  click: [project: Project]
}>()

const { getThumbnailUrl } = useYouTubeThumbnail()
const { getStatusLabel, getContinentLabel } = useProjectMappings()
const { getLocalizedText } = useMultilingual()

const localizedName = computed(() => {
  const name = props.project.name
  return typeof name === 'string' ? name : getLocalizedText(name, props.project.originalLang)
})

const localizedDescription = computed(() => {
  const desc = props.project.description
  return typeof desc === 'string' ? desc : getLocalizedText(desc, props.project.originalLang)
})

const thumbnailUrl = computed(() => {
  return props.project.yt ? getThumbnailUrl(props.project.yt) : null
})

const descriptionClampClass = computed(() => {
  const nameLength = localizedName.value.length

  if (nameLength >= 170) {
    return 'hide-description'
  } else if (nameLength >= 140) {
    return 'line-clamp-1'
  } else if (nameLength >= 110) {
    return 'line-clamp-3'
  } else if (nameLength >= 80) {
    return 'line-clamp-4'
  } else {
    return 'line-clamp-5'
  }
})

const getStatusColor = (status: string) => {
  switch (status) {
    case 'pending':
      return 'grey'
    case 'published':
      return 'blue'
    case 'stale':
      return 'orange'
    case 'verified':
      return 'green'
    case 'new':
      return 'purple'
    default:
      return 'grey'
  }
}

const handleClick = () => {
  emit('click', props.project)
}
</script>

<style scoped>
.hide-description {
  display: none;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-4 {
  display: -webkit-box;
  -webkit-line-clamp: 4;
  line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-5 {
  display: -webkit-box;
  -webkit-line-clamp: 5;
  line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-6 {
  display: -webkit-box;
  -webkit-line-clamp: 6;
  line-clamp: 6;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Project card styling - UNIFORM HEIGHT */
.project-card {
  position: relative;
  height: 320px;
  cursor: pointer;
  overflow: hidden;
  transition:
    transform 0.3s ease,
    box-shadow 0.3s ease;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3) !important;
}

/* Background image/gradient */
.project-card-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  transition: transform 0.5s ease;
}

.project-card:hover .project-card-bg {
  transform: scale(1.05);
}

/* Content overlay - visible on hover */
.project-card-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.9));
  color: white;
  padding: 20px;
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 3;
  display: flex;
  flex-direction: column;
  justify-content: center;
  overflow-y: auto;
}

.project-card:hover .project-card-overlay {
  opacity: 1;
}

.overlay-content {
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.chip-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* Smooth scrolling for overlay content */
.project-card-overlay::-webkit-scrollbar {
  width: 6px;
}

.project-card-overlay::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.1);
  border-radius: 3px;
}

.project-card-overlay::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
}

.project-card-overlay::-webkit-scrollbar-thumb:hover {
  background: rgba(255, 255, 255, 0.5);
}

/* Traditional card styling */
.project-card-traditional {
  position: relative;
  display: flex;
  background: white;
}

.traditional-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  width: 100%;
  padding: 24px;
}

.traditional-top {
  display: flex;
  align-items: flex-start;
}

.traditional-middle {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.traditional-middle h3 {
  line-height: 1.3;
  margin-bottom: 12px;
}

.traditional-bottom {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  align-items: flex-end;
}
</style>
