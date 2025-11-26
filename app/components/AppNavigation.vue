<template>
  <v-app-bar :elevation="2" color="surface" class="border-b">
    <v-container class="d-flex align-center">
      <!-- Logo -->
      <NuxtLink :to="localePath('/')" class="d-flex align-center text-decoration-none">
        <img src="/logo.png" alt="The Socioscope" class="logo mr-4" />
        <span class="text-h6 text-accent-lighten-1 font-weight-medium d-none d-sm-flex">
          {{ $t('hero.title') }}
        </span>
      </NuxtLink>

      <v-spacer />

      <!-- Desktop Navigation -->
      <v-toolbar-items class="d-none d-md-flex">
        <v-btn
          v-for="item in navItems"
          :key="item.key"
          :to="localePath(item.to)"
          variant="text"
          color="accent-lighten-1"
        >
          {{ $t(`nav.${item.key}`) }}
        </v-btn>
      </v-toolbar-items>

      <!-- Language Selector -->
      <LanguageSelector class="ml-4" />

      <!-- Mobile Menu Toggle -->
      <v-app-bar-nav-icon class="d-md-none ml-2" @click="drawer = !drawer" />
    </v-container>
  </v-app-bar>

  <!-- Mobile Drawer -->
  <v-navigation-drawer v-model="drawer" temporary location="right">
    <v-list>
      <v-list-item
        v-for="item in navItems"
        :key="item.key"
        :to="localePath(item.to)"
        @click="drawer = false"
      >
        <v-list-item-title>{{ $t(`nav.${item.key}`) }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const localePath = useLocalePath()
const drawer = ref(false)

const navItems = [
  { key: 'about', to: '/about' },
  { key: 'projects', to: '/projects' },
  { key: 'insights', to: '/insights' },
  { key: 'partners', to: '/partners' },
  { key: 'contact', to: '/contact' }
]
</script>

<style scoped lang="scss">
.border-b {
  border-bottom: 1px solid rgb(var(--v-theme-accent-lighten-2));
}

.logo {
  height: 50px;
  width: auto;
}

:deep(.v-btn) {
  text-transform: none;
}
</style>
