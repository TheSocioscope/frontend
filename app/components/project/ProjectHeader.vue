<template>
  <div class="project-header">
    <v-container>
      <div class="header-content">
        <div class="logo">
          <v-img
            v-if="project.logo"
            :src="resolveImagePath(project.logo)"
            :alt="localizedName"
            cover
          />
          <div v-else class="logo-placeholder">🌱</div>
        </div>

        <div class="header-info">
          <h1 class="initiative-name">{{ localizedName }}</h1>

          <div v-if="project.location" class="location">
            <v-icon size="small">mdi-map-marker</v-icon>
            {{ project.location }}
          </div>

          <div class="tags">
            <span v-if="project.status" class="tag">
              <v-icon size="small">mdi-check-circle</v-icon>
              {{ getStatusLabel(project.status) }}
            </span>

            <span v-for="continent in project.continent" :key="continent" class="tag">
              <v-icon size="small">mdi-earth</v-icon>
              {{ getContinentLabel(continent) }}
            </span>

            <span v-for="country in project.country" :key="country" class="tag">
              <v-icon size="small">mdi-map-marker</v-icon>
              {{ getCountryLabel(country) }}
            </span>

            <span v-for="field in project.field" :key="field" class="tag">
              <v-icon size="small">mdi-book-open-variant</v-icon>
              {{ getFieldLabel(field) }}
            </span>

            <span v-for="thematic in project.thematic" :key="thematic" class="tag">
              <v-icon size="small">mdi-tag</v-icon>
              {{ getThematicLabel(thematic) }}
            </span>

            <span v-for="type in project.type" :key="type" class="tag">
              <v-icon size="small">mdi-shape</v-icon>
              {{ getTypeLabel(type) }}
            </span>
          </div>

          <div v-if="project.url || project.contact" class="social-links">
            <a v-if="project.url" :href="project.url" target="_blank" class="social-link">
              <v-icon>mdi-web</v-icon>
            </a>

            <a
              v-if="project.contact?.contact_url"
              :href="project.contact.contact_url"
              target="_blank"
              class="social-link"
            >
              <v-icon>mdi-email</v-icon>
            </a>
          </div>
        </div>
      </div>
    </v-container>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  project: any
  localizedName: string
  showOriginal: boolean
  showDisclaimer: boolean
}>()

defineEmits<{
  'toggle-language': []
}>()

const { t: $t } = useI18n()
const { resolveImagePath } = useImagePath()
const {
  getStatusLabel,
  getContinentLabel,
  getCountryLabel,
  getFieldLabel,
  getThematicLabel,
  getTypeLabel
} = useProjectMappings()
</script>

<style scoped lang="scss">
.project-header {
  background-color: #f5edd6;
  padding: 60px 0 40px;
  :deep(.v-container) {
    max-width: 1400px;
  }
}

.header-content {
  display: flex;
  align-items: flex-start;
  gap: 30px;
  flex-wrap: wrap;
}

.logo {
  width: 120px;
  height: 120px;
  background-color: #fffbf0;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #4ca049;
  flex-shrink: 0;
  overflow: hidden;
}

.logo-placeholder {
  font-size: 48px;
}

.header-info {
  flex: 1;
  min-width: 250px;
}

.initiative-name {
  font-size: 2.5em;
  font-weight: 700;
  color: #27421d;
  margin-bottom: 10px;
}

.location {
  font-size: 1.2em;
  color: #2c2416;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.tag {
  background-color: #4ca049;
  color: #fffbf0;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9em;
  display: flex;
  align-items: center;
  gap: 6px;
}

.social-links {
  display: flex;
  gap: 15px;
}

.social-link {
  color: #27421d;
  font-size: 1.5em;
  transition: color 0.3s;
  text-decoration: none;

  &:hover {
    color: #4ca049;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
  }

  .initiative-name {
    font-size: 1.8em;
  }
}
</style>
