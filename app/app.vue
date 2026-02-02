<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup lang="ts">
// Global app configuration
const { resolveImagePath } = useImagePath()

useHead({
  titleTemplate: '%s | The Socioscope',
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'format-detection', content: 'telephone=no' }
  ],
  link: [{ rel: 'icon', type: 'image/x-icon', href: resolveImagePath('/favicon.ico') }]
})
</script>
