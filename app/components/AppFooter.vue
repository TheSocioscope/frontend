<template>
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <!-- About Column -->
        <div class="footer-column">
          <h4>{{ $t('footer.about.title') }}</h4>
          <ul>
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
        <div class="footer-column">
          <h4>
            <NuxtLink :to="localePath('/projects')">{{ $t('footer.explore.title') }}</NuxtLink>
          </h4>
          <ul>
            <li>
              <NuxtLink :to="localePath('/projects')">{{ $t('nav.database') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/products')">{{ $t('nav.products') }}</NuxtLink>
            </li>
            <li>
              <NuxtLink :to="localePath('/press')">{{ $t('nav.press') }}</NuxtLink>
            </li>
          </ul>
        </div>

        <!-- Resources Column -->
        <div class="footer-column">
          <h4>
            <NuxtLink :to="localePath('/resources')">{{ $t('footer.resources.title') }}</NuxtLink>
          </h4>
          <ul>
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
        <div class="footer-column">
          <h4>
            <NuxtLink :to="localePath('/contact')">{{ $t('nav.contact') }}</NuxtLink>
          </h4>
          <ul>
            <li>
              <a href="#newsletter">{{ $t('footer.connect.newsletter') }}</a>
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
        <p>{{ $t('footer.copyright', { year: currentYear }) }}</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { socials } from '~~/static.config'

const { t: $t } = useI18n()
const localePath = useLocalePath()
const currentYear = new Date().getFullYear()
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.site-footer {
  background: $brown-dark;
  color: $cream;
  padding: 4rem 0 2rem;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 2rem;
}

.footer-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 3rem;
  margin-bottom: 3rem;

  @media (max-width: 960px) {
    grid-template-columns: repeat(2, 1fr);
  }

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.footer-column {
  h4 {
    font-family: $font-family-display;
    font-size: 1.25rem;
    margin-bottom: 1.5rem;
    color: $green-bright;

    a {
      color: $green-bright;
      text-decoration: none;
      transition: color 0.3s;

      &:hover {
        color: $warm-beige;
      }
    }
  }

  ul {
    list-style: none;
    padding: 0;
    margin: 0;

    li {
      margin-bottom: 0.75rem;
    }
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

.footer-bottom {
  text-align: center;
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 251, 240, 0.1);

  p {
    color: $warm-beige;
    margin: 0;
    font-size: 0.9rem;
  }
}
</style>
