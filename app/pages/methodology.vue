<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <h1 class="text-h2 mb-8">{{ $t('pages.methodology') }}</h1>

        <v-card elevation="2" class="pa-8">
          <div class="prose">
            <p class="text-body-1 mb-4">
              The Socioscope methodology combines rigorous social science research with innovative
              computational approaches to understand social transformation.
            </p>

            <h2 class="text-h4 mt-8 mb-4">Research Framework</h2>
            <p class="text-body-1 mb-4">Our research framework is built on three pillars:</p>
            <ul class="mb-6">
              <li>Systematic case documentation</li>
              <li>Network analysis</li>
              <li>Comparative research</li>
            </ul>

            <h2 class="text-h4 mt-8 mb-4">Data Collection</h2>
            <p class="text-body-1 mb-4">
              We employ a multi-method approach combining qualitative and quantitative methods to
              capture the complexity of social change processes.
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
  title: t('pages.methodology')
})
</script>
