<template>
  <header class="site-header">
    <nav class="nav-container container">
      <!-- Logo with animated circles -->
      <NuxtLink :to="localePath('/')" class="logo-container">
        <div class="logo-circle logo-circle-1" />
        <div class="logo-circle logo-circle-2" />
        <div class="logo-circle logo-circle-3" />
        <span class="logo-text">THE SOCIOSCOPE</span>
      </NuxtLink>

      <!-- Desktop Navigation -->
      <ul class="nav-links d-none d-md-flex">
        <li class="dropdown">
          <a href="#about">{{ $t('nav.about') }}</a>
          <div class="dropdown-content">
            <NuxtLink :to="localePath('/about')">{{ $t('nav.socioscope') }}</NuxtLink>
            <NuxtLink :to="localePath('/team')">{{ $t('nav.team') }}</NuxtLink>
            <NuxtLink :to="localePath('/faq')">{{ $t('nav.faq') }}</NuxtLink>
          </div>
        </li>
        <li class="dropdown">
          <NuxtLink :to="localePath('/projects')">{{ $t('nav.projects') }}</NuxtLink>
          <div class="dropdown-content">
            <NuxtLink :to="localePath('/projects')">{{ $t('nav.database') }}</NuxtLink>
            <NuxtLink :to="localePath('/projects')">{{ $t('nav.submitInitiative') }}</NuxtLink>
          </div>
        </li>
        <li>
          <NuxtLink :to="localePath('/products')">{{ $t('nav.products') }}</NuxtLink>
        </li>
        <li class="dropdown">
          <NuxtLink :to="localePath('/resources')">{{ $t('nav.resources') }}</NuxtLink>
          <div class="dropdown-content">
            <NuxtLink :to="localePath('/resources?filter=article')">{{
              $t('nav.articles')
            }}</NuxtLink>
            <NuxtLink :to="localePath('/resources?filter=book')">{{ $t('nav.books') }}</NuxtLink>
            <NuxtLink :to="localePath('/resources?filter=event')">{{ $t('nav.events') }}</NuxtLink>
          </div>
        </li>
        <li class="dropdown">
          <a href="#contact">{{ $t('nav.contact') }}</a>
          <div class="dropdown-content">
            <NuxtLink :to="localePath('/contact')">{{ $t('nav.contactUs') }}</NuxtLink>
            <NuxtLink :to="localePath('/press')">{{ $t('nav.press') }}</NuxtLink>
          </div>
        </li>
      </ul>

      <!-- Language Selector -->
      <LanguageSelector class="language-selector-wrapper" />

      <!-- Mobile Menu Toggle -->
      <button class="mobile-menu-toggle d-md-none" @click="drawer = !drawer">
        <span class="menu-icon">☰</span>
      </button>
    </nav>
  </header>

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
  { key: 'products', to: '/products' },
  { key: 'contact', to: '/contact' }
]
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.site-header {
  background: $cream;
  padding: 1.5rem 0;
  border-bottom: 1px solid $warm-beige;
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(10px);
}

.nav-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  position: relative;
  width: 200px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
}

.logo-text {
  font-family: $font-family-display;
  font-size: 1.3rem;
  font-weight: $font-weight-bold;
  letter-spacing: 0.05em;
  color: $brown-dark;
  position: relative;
  z-index: 2;
}

.logo-circle {
  position: absolute;
  border-radius: 50%;
  border: 1.5px solid;
  opacity: 0.2;

  &-1 {
    width: 30px;
    height: 30px;
    border-color: $green-bright;
    animation: logoPulse 3s ease-in-out infinite;
  }

  &-2 {
    width: 45px;
    height: 45px;
    border-color: $forest-green;
    animation: logoPulse 3s ease-in-out 1s infinite;
  }

  &-3 {
    width: 60px;
    height: 60px;
    border-color: $brown-dark;
    animation: logoPulse 3s ease-in-out 2s infinite;
  }
}

@keyframes logoPulse {
  0%,
  100% {
    transform: scale(1);
    opacity: 0.2;
  }
  50% {
    transform: scale(1.15);
    opacity: 0.35;
  }
}

.nav-links {
  display: flex;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;

  > li {
    position: relative;
  }

  a {
    color: $brown-dark;
    text-decoration: none;
    font-weight: $font-weight-medium;
    font-size: 1.3rem;
    transition: color 0.3s;

    &:hover {
      color: $green-bright;
    }
  }
}

.dropdown {
  position: relative;

  > a::after {
    content: ' ▾';
    font-size: 0.8rem;
  }

  // Add a pseudo-element to bridge the gap between trigger and dropdown
  &::before {
    content: '';
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    height: 0.25rem;
    display: none;
  }

  &:hover::before {
    display: block;
  }
}

.dropdown-content {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: $cream;
  min-width: 250px;
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
  border: 1px solid $warm-beige;
  border-radius: 4px;
  padding: 0.5rem 0;
  margin-top: 0.25rem;
  z-index: 1000;

  a {
    display: block;
    padding: 0.75rem 1.5rem;
    color: $brown-dark;
    text-decoration: none;
    transition:
      background 0.3s,
      color 0.3s;
    font-size: 1.3rem;
    white-space: nowrap;

    &:hover {
      background: $warm-beige;
      color: $green-bright;
    }
  }
}

.dropdown:hover .dropdown-content,
.dropdown-content:hover {
  display: block;
}

.language-selector-wrapper {
  margin-left: 1rem;
}

.mobile-menu-toggle {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: $brown-dark;
  cursor: pointer;
  padding: 0.5rem;
}

@media (max-width: 960px) {
  .nav-links {
    display: none;
  }

  .logo-container {
    width: auto;
  }
}
</style>
