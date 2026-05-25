<template>
  <div class="galaxy-empty" role="status">
    <v-icon size="40" color="primary">mdi-filter-off-outline</v-icon>
    <p class="empty-title">{{ $t('galaxy.emptyTitle', 'No initiatives match these filters') }}</p>
    <p class="empty-body">
      {{ $t('galaxy.emptyBody', 'Adjust filters to see initiatives appear in the galaxy.') }}
    </p>
    <v-btn
      v-if="canReset"
      variant="outlined"
      color="primary"
      prepend-icon="mdi-close-circle"
      @click="$emit('reset')"
    >
      {{ $t('common.resetFilters', 'Reset filters') }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  canReset?: boolean
}>()

defineEmits<{
  reset: []
}>()

const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.galaxy-empty {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: $spacing-sm;
  padding: $spacing-md;
  text-align: center;
  background: rgba(248, 249, 250, 0.92);
  z-index: 3;
  pointer-events: auto;

  .empty-title {
    margin: 0;
    font-size: 1.0625rem;
    font-weight: 600;
    color: $green-dark;
  }

  .empty-body {
    margin: 0;
    color: rgba(0, 0, 0, 0.6);
    font-size: 0.875rem;
    max-width: 320px;
  }
}
</style>
