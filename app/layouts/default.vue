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
  border-radius: 0 !important;
  border: 2px solid green !important;
  background-color: white !important;
}

.scroll-to-top-btn :deep(.v-icon) {
  color: green !important;
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
