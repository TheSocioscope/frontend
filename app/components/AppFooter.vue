<template>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <!-- About Column -->
        <div class="footer-column" :class="{ open: isOpen('about') }">
          <button
            type="button"
            class="footer-column__toggle"
            :aria-expanded="isOpen('about')"
            aria-controls="footer-col-about"
            @click="toggle('about')"
          >
            <h4>{{ $t('footer.about.title') }}</h4>
            <svg class="footer-column__chevron" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8 10l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2" />
            </svg>
          </button>
          <ul id="footer-col-about">
            <li>
              <NuxtLink :to="localePath('/about')">{{ $t('nav.socioscope') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/team')">{{ $t('footer.team') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/faq')">{{ $t('nav.faq') }}</NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Explore Column -->
        <div class="footer-column" :class="{ open: isOpen('explore') }">
          <button
            type="button"
            class="footer-column__toggle"
            :aria-expanded="isOpen('explore')"
            aria-controls="footer-col-explore"
            @click="toggle('explore')"
          >
            <h4>{{ $t('footer.explore.title') }}</h4>
            <svg class="footer-column__chevron" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8 10l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2" />
            </svg>
          </button>
          <ul id="footer-col-explore">
            <li>
              <NuxtLink :to="localePath('/projects')">{{ $t('nav.database') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/products')">{{ $t('nav.products') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/research')">{{ $t('nav.research', 'Research') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/press')">{{ $t('nav.press') }}</NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Resources Column -->
        <div class="footer-column" :class="{ open: isOpen('resources') }">
          <button
            type="button"
            class="footer-column__toggle"
            :aria-expanded="isOpen('resources')"
            aria-controls="footer-col-resources"
            @click="toggle('resources')"
          >
            <h4>{{ $t('footer.resources.title') }}</h4>
            <svg class="footer-column__chevron" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8 10l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2" />
            </svg>
          </button>
          <ul id="footer-col-resources">
            <li>
              <NuxtLink :to="localePath('/resources')">{{ $t('nav.resources') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/resources?filter=article')">{{
                $t('nav.articles')
              }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/resources?filter=book')">{{ $t('nav.books') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/resources?filter=event')">{{
                $t('nav.events')
              }}</NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Contact Column -->
        <div class="footer-column" :class="{ open: isOpen('contact') }">
          <button
            type="button"
            class="footer-column__toggle"
            :aria-expanded="isOpen('contact')"
            aria-controls="footer-col-contact"
            @click="toggle('contact')"
          >
            <h4>{{ $t('nav.contact') }}</h4>
            <svg class="footer-column__chevron" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M8 10l4 4 4-4" fill="none" stroke="currentColor" stroke-width="2" />
            </svg>
          </button>
          <ul id="footer-col-contact">
            <li>
              <NuxtLink :to="localePath('/contact')">{{ $t('nav.contactUs') }}</NuxtLink>
            </li>
            <li v-if="socials.linkedin">
              <a :href="socials.linkedin" target="_blank" rel="noopener noreferrer">{{
                $t('footer.connect.linkedin')
              }}</a>
            </li>
            <li v-if="socials.youtube">
              <a :href="socials.youtube" target="_blank" rel="noopener noreferrer">YouTube</a>
            </li>
            <li v-if="socials.github">
              <a :href="socials.github" target="_blank" rel="noopener noreferrer">{{
                $t('footer.connect.github')
              }}</a>
            </li>
          </ul>
        </div>
      </div>

      <!-- Copyright -->
      <div class="footer-bottom">
        <p>
          {{ $t('footer.copyright', { year: currentYear }) }} ·
          <NuxtLink :to="localePath('/privacy')">{{ $t('footer.privacy') }}</NuxtLink>
          ·
          <NuxtLink :to="localePath('/terms')">{{ $t('footer.terms') }}</NuxtLink>
          ·
          <NuxtLink to="/mentions-legales">{{ $t('footer.mentionsLegales') }}</NuxtLink>
        </p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { socials } from '~~/static.config'

const { t: $t } = useI18n()
const localePath = useLocalePath()
const currentYear = new Date().getFullYear()

// Footer columns collapse into an accordion on mobile only (see <= 768px styles
// below). On desktop the lists are always visible and the toggle is inert.
type FooterSection = 'about' | 'explore' | 'resources' | 'contact'
const openSections = ref<Set<FooterSection>>(new Set())
const isOpen = (section: FooterSection) => openSections.value.has(section)
const toggle = (section: FooterSection) => {
  const next = new Set(openSections.value)
  next.has(section) ? next.delete(section) : next.add(section)
  openSections.value = next
}
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.site-footer {
  background: $brown-dark;
  color: $cream;
  padding: 4rem 0 2rem;

  @media (max-width: 768px) {
    padding: 2rem 0 1.25rem;
  }
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;

  @media (max-width: 768px) {
    padding: 0 1.25rem;
  }
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 3rem;
  margin-bottom: 3rem;

  @media (max-width: 960px) {
    grid-template-columns: repeat(2, 1fr);
    gap: 2rem 1.5rem;
    margin-bottom: 2rem;
  }

  // On phones each column is a collapsed accordion row, so stack them in
  // a single column instead of cramming two side by side.
  @media (max-width: 768px) {
    grid-template-columns: 1fr;
    gap: 0;
    margin-bottom: 1.5rem;
  }
}

.footer-column {
  min-width: 0;

  &__toggle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.5rem;
    width: 100%;
    padding: 0;
    background: none;
    border: none;
    text-align: left;
    color: inherit;
    cursor: default;
  }

  // The chevron + tap-to-expand behaviour only exists on mobile.
  &__chevron {
    display: none;
    flex-shrink: 0;
    width: 1.25rem;
    height: 1.25rem;
    color: $green-bright;
    transition: transform 0.3s;
  }

  h4 {
    font-family: $font-family-display;
    font-size: 1.25rem;
    margin: 0 0 1rem;
    color: $green-bright;
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;

    li {
      margin-bottom: 0.625rem;
    }
  }

  a {
    color: $warm-beige;
    text-decoration: none;
    transition: color 0.3s;
    font-size: 0.95rem;

    &:hover {
      color: $green-bright;
    }
  }

  @media (max-width: 768px) {
    padding: 1rem 0;
    border-bottom: 1px solid rgba(255, 251, 240, 0.1);

    &:last-child {
      border-bottom: none;
    }

    &__toggle {
      cursor: pointer;
    }

    &__toggle h4 {
      margin-bottom: 0;
    }

    &.open &__toggle h4 {
      margin-bottom: 0.75rem;
    }

    &__chevron {
      display: block;
    }

    &.open &__chevron {
      transform: rotate(180deg);
    }

    h4 {
      font-size: 1rem;
    }

    // Collapsed by default on mobile; the column gets `.open` when tapped.
    ul {
      display: none;

      li {
        margin-bottom: 0.5rem;
      }
    }

    &.open ul {
      display: block;
    }

    a {
      font-size: 0.875rem;
    }
  }
}

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 251, 240, 0.1);

  @media (max-width: 768px) {
    padding-top: 1.25rem;
  }

  p {
    color: $warm-beige;
    margin: 0;
    font-size: 0.9rem;

    @media (max-width: 768px) {
      font-size: 0.8rem;
    }

    a {
      color: $warm-beige;
      text-decoration: none;
      transition: color 0.3s;

      &:hover {
        color: $green-bright;
      }
    }
  }
}
</style>
