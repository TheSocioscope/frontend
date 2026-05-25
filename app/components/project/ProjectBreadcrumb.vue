<template>
  <nav class="project-breadcrumb" aria-label="Breadcrumb">
    <v-container class="breadcrumb-container">
      <NuxtLink :to="localePath('/projects')" class="back-link">
        <v-icon size="small">mdi-arrow-left</v-icon>
        <span>{{ $t('nav.projects') }}</span>
      </NuxtLink>
      <span class="separator" aria-hidden="true">·</span>
      <span class="current">{{ localizedName }}</span>

      <v-menu location="bottom end">
        <template #activator="{ props: activator }">
          <v-btn
            class="kebab"
            icon="mdi-dots-vertical"
            variant="text"
            size="small"
            density="comfortable"
            v-bind="activator"
            :aria-label="$t('editDrawer.title')"
          />
        </template>
        <v-list density="compact">
          <v-list-item @click="emit('edit')">
            <template #prepend>
              <v-icon size="small">mdi-pencil</v-icon>
            </template>
            <v-list-item-title>{{ $t('editDrawer.title') }}</v-list-item-title>
          </v-list-item>
          <v-list-item @click="copyLink">
            <template #prepend>
              <v-icon size="small">mdi-content-copy</v-icon>
            </template>
            <v-list-item-title>
              {{ copied ? $t('common.copied') : $t('common.copyLink') }}
            </v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-container>
  </nav>
</template>

<script setup lang="ts">
const props = defineProps<{
  localizedName: string
  pageUrl: string
}>()

const emit = defineEmits<{ edit: [] }>()

const { t: $t } = useI18n()
const localePath = useLocalePath()
const copied = ref(false)

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(props.pageUrl || window.location.href)
    copied.value = true
    setTimeout(() => (copied.value = false), 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-breadcrumb {
  position: sticky;
  top: $sticky-site-header;
  z-index: 9;
  background: var(--page-bg, #f8f9fa);
  border-bottom: 1px solid $border-soft;
  height: $sticky-breadcrumb;
  display: flex;
  align-items: center;
}

.breadcrumb-container {
  display: flex;
  align-items: center;
  gap: $rhythm-1;
  max-width: $container-max-detail;
  font-size: 0.875rem;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  color: $green-dark;
  text-decoration: none;
  font-weight: 500;

  &:hover {
    text-decoration: underline;
  }

  &:focus-visible {
    outline: 2px solid $green-dark;
    outline-offset: 2px;
    border-radius: 2px;
  }
}

.separator {
  color: rgba(0, 0, 0, 0.35);
}

.current {
  color: $text-secondary;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  min-width: 0;
}

.kebab {
  margin-left: auto;
}
</style>
