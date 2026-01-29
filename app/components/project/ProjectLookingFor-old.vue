<template>
  <v-card
    v-if="localizedLookingFor && localizedLookingFor.length > 0"
    id="looking-for"
    class="project-looking-for"
  >
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-account-search-outline</v-icon>
      {{ $t('common.lookingFor') }}
    </v-card-title>
    <v-card-text>
      <v-list class="looking-for-list">
        <v-list-item
          v-for="(item, index) in localizedLookingFor"
          :key="index"
          class="looking-for-item"
        >
          <template #prepend>
            <v-icon color="primary" size="large">mdi-checkbox-marked-circle-outline</v-icon>
          </template>

          <v-list-item-title class="item-title">
            {{ item.title }}
          </v-list-item-title>

          <v-list-item-subtitle v-if="item.description" class="item-description">
            {{ item.description }}
          </v-list-item-subtitle>
        </v-list-item>
      </v-list>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
defineProps<{
  localizedLookingFor: Array<{ title: string; description?: string }>
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
.project-looking-for {
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

.looking-for-list {
  padding: 0;
}

.looking-for-item {
  padding: 1rem;
  margin-bottom: 0.5rem;
  border-left: 3px solid rgb(var(--v-theme-primary));
  background: rgba(102, 126, 234, 0.03);
  border-radius: 4px;
  transition: all 0.2s ease;

  &:hover {
    background: rgba(102, 126, 234, 0.08);
    transform: translateX(4px);
  }
}

.item-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.87);
  margin-bottom: 0.25rem;
}

.item-description {
  font-size: 1rem;
  line-height: 1.5;
  color: rgba(0, 0, 0, 0.6);
  margin-top: 0.5rem;
  white-space: normal;
}
</style>
