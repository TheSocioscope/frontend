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
            <!--             <span v-if="project.status" class="tag">
              <v-icon size="small">mdi-check-circle</v-icon>
              {{ getStatusLabel(project.status) }}
            </span> -->

            <span v-for="continent in project.continent" :key="continent" class="tag">
              <v-icon size="small">mdi-earth</v-icon>
              {{ getContinentLabel(continent) }}
            </span>

            <span v-for="country in project.country" :key="country" class="tag">
              <v-icon size="small">mdi-map-marker</v-icon>
              {{ getCountryLabel(country) }}
            </span>

            <span v-for="role in project.entityRole" :key="role" class="tag">
              <v-icon size="small">mdi-account-hard-hat</v-icon>
              {{ role }}
            </span>

            <span v-if="project.bizModel" class="tag">
              <v-icon size="small">mdi-domain</v-icon>
              {{ project.bizModel }}
            </span>

            <span v-if="project.entitySize" class="tag">
              <v-icon size="small">mdi-resize</v-icon>
              {{ project.entitySize }}
            </span>

            <span v-if="project.geoReach" class="tag">
              <v-icon size="small">mdi-map-search</v-icon>
              {{ project.geoReach }}
            </span>

            <span v-for="sector in project.sectorFocus" :key="sector" class="tag">
              <v-icon size="small">mdi-sprout</v-icon>
              {{ sector }}
            </span>

            <span v-if="project.resourceType" class="tag">
              <v-icon size="small">mdi-package-variant</v-icon>
              {{ project.resourceType }}
            </span>
          </div>

          <div class="social-links">
            <a v-if="project.url" :href="project.url" target="_blank" class="social-link" title="Visit website">
              <v-icon>mdi-web</v-icon>
            </a>

            <a
              v-if="project.contact?.contact_url"
              :href="project.contact.contact_url"
              target="_blank"
              class="social-link"
              title="Email"
            >
              <v-icon>mdi-email</v-icon>
            </a>

            <button class="social-link connect-link" title="Connect with this initiative" @click="$emit('connect')">
              <v-icon>mdi-human-greeting-proximity</v-icon>
            </button>
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
  'connect': []
}>()

const { t: $t } = useI18n()
const { resolveImagePath } = useImagePath()
const { getContinentLabel, getCountryLabel } = useProjectMappings()
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

.connect-link {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  display: inline-flex;
  align-items: center;
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
