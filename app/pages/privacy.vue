<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <h1 class="text-h2 mb-8">{{ $t('pages.privacy') }}</h1>

        <v-card elevation="2" class="pa-8">
          <div class="prose">
            <h2 class="text-h4 mb-4">Privacy Policy</h2>
            <p class="text-body-1 mb-4">Last updated: November 26, 2025</p>

            <h3 class="text-h5 mt-6 mb-3">Information We Collect</h3>
            <p class="text-body-1 mb-4">
              We collect information that you provide directly to us, including when you subscribe
              to our newsletter, contact us, or participate in our research.
            </p>

            <h3 class="text-h5 mt-6 mb-3">How We Use Your Information</h3>
            <p class="text-body-1 mb-4">
              We use the information we collect to communicate with you, conduct research, and
              improve our services.
            </p>

            <h3 class="text-h5 mt-6 mb-3">Data Security</h3>
            <p class="text-body-1 mb-4">
              We implement appropriate security measures to protect your personal information.
            </p>

            <h3 class="text-h5 mt-6 mb-3">Contact Us</h3>
            <p class="text-body-1">
              If you have questions about this privacy policy, please contact us.
            </p>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: t('pages.privacy')
})
</script>
