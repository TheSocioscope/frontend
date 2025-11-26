<template>
  <div>
    <v-container class="py-16">
      <h1 class="text-h2 text-center mb-8">{{ $t('pages.about') }}</h1>
      <div class="content-section">
        <p class="text-h5 text-center mb-8">Coming soon</p>
      </div>
    </v-container>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

useHead({
  title: $t('pages.about')
})
</script>
