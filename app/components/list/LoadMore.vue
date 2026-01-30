<template>
  <div v-if="hasMore" class="load-more">
    <button class="load-more-btn" :disabled="loading" @click="emit('load-more')">
      {{ loading ? loadingLabel : label }}
    </button>
  </div>
</template>

<script setup lang="ts">
interface Props {
  hasMore: boolean
  loading?: boolean
  label?: string
  loadingLabel?: string
}

withDefaults(defineProps<Props>(), {
  loading: false,
  label: 'Load More',
  loadingLabel: 'Loading...'
})

const emit = defineEmits<{
  'load-more': []
}>()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/pagination' as *;
</style>
