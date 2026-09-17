<template>
  <span>{{ count }}</span>
</template>

<script setup lang="ts">
// Global so Markdown content can use it inline: `:initiative-count`
const count = await useInitiativeCount()
</script>
