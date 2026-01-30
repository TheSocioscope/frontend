<template>
  <div class="results-info">
    <slot :start="start" :end="end" :total="total">
      {{ message }}
    </slot>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  start: number
  end: number
  total: number
  message?: string
}

const props = defineProps<Props>()

const message = computed(() => {
  if (props.message) return props.message
  return `Showing ${props.start}-${props.end} of ${props.total}`
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/pagination' as *;
</style>
