<template>
  <v-app>
    <AppNavigation />
    <v-main>
      <slot />
    </v-main>
    <AppFooter />
  </v-app>
</template>

<script setup lang="ts">
// Set page language based on current locale
const { locale } = useI18n()

useHead({
  htmlAttrs: {
    lang: locale.value
  }
})
</script>
