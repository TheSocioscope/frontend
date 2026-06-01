<template>
  <v-app>
    <AppNavigation />

    <v-main>
      <slot />
      <!-- Scroll to top FAB -->
      <v-tooltip :text="$t('Scroll to top')" location="left">
        <template #activator="{ props }">
          <v-btn
            v-show="showScrollToTop"
            v-bind="props"
            class="scroll-to-top-btn"
            icon="mdi-arrow-up"
            size="large"
            @click="scrollToTop"
          />
        </template>
      </v-tooltip>
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

// Scroll to top functionality
const showScrollToTop = ref(false)

const handleScroll = () => {
  if (process.client) {
    showScrollToTop.value = window.scrollY > 200
  }
}

const scrollToTop = () => {
  if (process.client) {
    window.scrollTo({
      top: 0,
      behavior: 'smooth'
    })
  }
}

onMounted(() => {
  if (process.client) {
    window.addEventListener('scroll', handleScroll, { passive: true })
  }
})

onUnmounted(() => {
  if (process.client) {
    window.removeEventListener('scroll', handleScroll)
  }
})
</script>

<style scoped>
.scroll-to-top-btn {
  position: fixed !important;
  bottom: 24px !important;
  right: 24px !important;
  z-index: 1000 !important;
  border-radius: 50% !important;
  background-color: white !important;
  border: 0.5px solid #d0d0d0 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12) !important;
}

.scroll-to-top-btn :deep(.v-icon) {
  color: #27421d !important;
}

@media (max-width: 600px) {
  .scroll-to-top-btn {
    bottom: 16px !important;
    right: 16px !important;
    width: 40px !important;
    height: 40px !important;
  }

  .scroll-to-top-btn :deep(.v-icon) {
    font-size: 20px !important;
  }
}
</style>
