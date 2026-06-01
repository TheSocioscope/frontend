<template>
  <nav class="project-breadcrumb" aria-label="Breadcrumb">
    <v-container class="breadcrumb-container">
      <NuxtLink :to="localePath('/projects')" class="back-link">
        <v-icon size="small">mdi-arrow-left</v-icon>
        <span>{{ $t('nav.projects') }}</span>
      </NuxtLink>
    </v-container>
  </nav>
</template>

<script setup lang="ts">
defineProps<{
  localizedName: string
  pageUrl: string
}>()

const { t: $t } = useI18n()
const localePath = useLocalePath()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-breadcrumb {
  position: sticky;
  top: $sticky-site-header;
  z-index: 9;
  background: var(--page-bg, #f8f9fa);
  height: $sticky-breadcrumb;
  display: flex;
  align-items: center;
}

.breadcrumb-container {
  display: flex;
  align-items: center;
  max-width: $container-max-detail;
  font-size: 0.875rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: $green-forest;
  text-decoration: none;
  font-weight: 600;

  &:hover {
    color: $green-leaf;
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid $green-leaf;
    outline-offset: 2px;
    border-radius: 2px;
  }
}
</style>
