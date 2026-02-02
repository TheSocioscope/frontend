<template>
  <div v-if="hasActiveFilters" class="filter-reset-container">
    <!-- Desktop: Button with text -->
    <v-btn
      v-if="!isMobile"
      prepend-icon="mdi-refresh"
      color="primary"
      variant="outlined"
      rounded="0"
      bg-color="white"
      class="reset-button"
      @click="resetFilters"
    >
      {{ $t('common.resetFilters') }}
    </v-btn>

    <!-- Mobile: Icon button with tooltip -->
    <v-tooltip v-else location="top">
      <template #activator="{ props }">
        <v-btn
          v-bind="props"
          icon="mdi-refresh"
          color="primary"
          variant="outlined"
          rounded="0"
          bg-color="white"
          class="reset-button-mobile"
          @click="resetFilters"
        />
      </template>
      <span>{{ $t('common.resetFilters') }}</span>
    </v-tooltip>
  </div>
</template>

<script setup lang="ts">
interface Props {
  hasActiveFilters: boolean
}

interface Emits {
  (e: 'reset'): void
}

defineProps<Props>()
const emit = defineEmits<Emits>()

const { t: $t } = useI18n()

const isMobile = ref(false)

onMounted(() => {
  isMobile.value = window.innerWidth < 768
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth < 768
  })
})

const resetFilters = () => {
  emit('reset')
}
</script>

<style scoped lang="scss">
.filter-reset-container {
  display: flex;
  justify-content: center;
  align-items: center;
}

.reset-button {
  height: 40px;
  aspect-ratio: auto;
}

.reset-button-mobile {
  width: 40px;
  height: 40px;
}
</style>
