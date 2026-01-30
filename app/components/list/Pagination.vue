<template>
  <div class="pagination">
    <button :disabled="currentPage === 1" class="pagination-btn" @click="emit('prev')">
      {{ previousLabel }}
    </button>

    <div class="pagination-pages">
      <button
        v-for="page in visiblePages"
        :key="page"
        :class="['pagination-btn', { active: page === currentPage, ellipsis: page === -1 }]"
        :disabled="page === -1"
        @click="page > 0 && emit('goto', page)"
      >
        {{ page === -1 ? '...' : page }}
      </button>
    </div>

    <button :disabled="currentPage === totalPages" class="pagination-btn" @click="emit('next')">
      {{ nextLabel }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  currentPage: number
  totalPages: number
  previousLabel?: string
  nextLabel?: string
}

const props = withDefaults(defineProps<Props>(), {
  previousLabel: 'Previous',
  nextLabel: 'Next'
})

const emit = defineEmits<{
  prev: []
  next: []
  goto: [page: number]
}>()

const visiblePages = computed(() => {
  const pages: number[] = []
  const total = props.totalPages
  const current = props.currentPage

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    if (current <= 4) {
      for (let i = 1; i <= 5; i++) {
        pages.push(i)
      }
      pages.push(-1) // ellipsis
      pages.push(total)
    } else if (current >= total - 3) {
      pages.push(1)
      pages.push(-1) // ellipsis
      for (let i = total - 4; i <= total; i++) {
        pages.push(i)
      }
    } else {
      pages.push(1)
      pages.push(-1) // ellipsis
      for (let i = current - 1; i <= current + 1; i++) {
        pages.push(i)
      }
      pages.push(-1) // ellipsis
      pages.push(total)
    }
  }

  return pages
})
</script>

<style scoped lang="scss">
@use '~~/assets/styles/pagination' as *;
</style>
