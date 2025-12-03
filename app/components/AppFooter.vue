<template>
  <v-footer class="footer" color="accent">
    <v-container>
      <v-row>
        <!-- About Column -->
        <v-col cols="12" md="3">
          <h4 class="footer-title">{{ $t('footer.about.title') }}</h4>
          <v-list density="compact" bg-color="transparent">
            <v-list-item
              v-for="item in aboutLinks"
              :key="item.key"
              :to="localePath(item.to)"
              class="footer-link"
            >
              {{ $t(`footer.about.${item.key}`) }}
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Explore Column -->
        <v-col cols="12" md="3">
          <h4 class="footer-title">{{ $t('footer.explore.title') }}</h4>
          <v-list density="compact" bg-color="transparent">
            <v-list-item
              v-for="item in exploreLinks"
              :key="item.key"
              :to="localePath(item.to)"
              class="footer-link"
            >
              {{ $t(`footer.explore.${item.key}`) }}
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Resources Column -->
        <v-col cols="12" md="3">
          <h4 class="footer-title">{{ $t('footer.resources.title') }}</h4>
          <v-list density="compact" bg-color="transparent">
            <v-list-item
              v-for="item in resourceLinks"
              :key="item.key"
              :to="localePath(item.to)"
              class="footer-link"
            >
              {{ $t(`footer.resources.${item.key}`) }}
            </v-list-item>
          </v-list>
        </v-col>

        <!-- Connect Column -->
        <v-col cols="12" md="3">
          <h4 class="footer-title">{{ $t('footer.connect.title') }}</h4>
          <v-list density="compact" bg-color="transparent">
            <v-list-item
              v-for="item in connectLinks"
              :key="item.key"
              :href="item.href"
              target="_blank"
              class="footer-link"
            >
              {{ $t(`footer.connect.${item.key}`) }}
            </v-list-item>
          </v-list>
        </v-col>
      </v-row>

      <!-- Copyright -->
      <v-divider class="my-6 border-opacity-25" />
      <v-row>
        <v-col class="text-center">
          <p class="footer-copyright">
            {{ $t('footer.copyright') }}
          </p>
        </v-col>
      </v-row>
    </v-container>
  </v-footer>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()
const localePath = useLocalePath()

const aboutLinks = [
  { key: 'about', to: '/about' },
  { key: 'methodology', to: '/methodology' },
  { key: 'team', to: '/team' },
  { key: 'publications', to: '/publications' }
]

const exploreLinks = [
  { key: 'database', to: '/projects' },
  { key: 'stories', to: '/stories' },
  { key: 'insights', to: '/insights' }
]

const resourceLinks = [
  { key: 'publications', to: '/publications' },
  { key: 'news', to: '/news-events' },
  { key: 'faq', to: '/faq' },
  { key: 'contact', to: '/contact' }
]

const connectLinks = [
  { key: 'newsletter', href: '#newsletter' },
  { key: 'twitter', href: 'https://twitter.com/thesocioscope' },
  { key: 'linkedin', href: 'https://linkedin.com/company/thesocioscope' },
  { key: 'github', href: 'https://github.com/thesocioscope' }
]
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.footer {
  padding: $spacing-4xl 0 $spacing-lg;

  :deep(.v-container) {
    color: $cream-light;
  }
}

.footer-title {
  color: $green-light-olive;
  font-size: 1.2rem;
  margin-bottom: $spacing-md;
  letter-spacing: 1px;
  padding-left: 1rem;
}

.footer-link {
  color: $cream-light !important;
  padding-left: 0;
  min-height: 32px;

  &:hover {
    color: $green-light-olive !important;
  }

  :deep(.v-list-item__content) {
    padding: 0;
  }
}

.footer-copyright {
  color: $brown-light;
  font-size: 0.9rem;
  margin: 0;
}
</style>
