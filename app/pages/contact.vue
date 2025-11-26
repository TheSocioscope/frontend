<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <h1 class="text-h2 mb-8">{{ $t('pages.contact') }}</h1>

        <v-card elevation="2" class="pa-8">
          <v-form @submit.prevent="handleSubmit">
            <v-text-field
              v-model="form.name"
              label="Name"
              variant="outlined"
              class="mb-4"
              required
            />

            <v-text-field
              v-model="form.email"
              label="Email"
              type="email"
              variant="outlined"
              class="mb-4"
              required
            />

            <v-text-field
              v-model="form.subject"
              label="Subject"
              variant="outlined"
              class="mb-4"
              required
            />

            <v-textarea
              v-model="form.message"
              label="Message"
              variant="outlined"
              rows="6"
              class="mb-4"
              required
            />

            <v-btn type="submit" color="primary" size="large" class="bg-primary-green">
              Send Message
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: t('pages.contact')
})

const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const handleSubmit = () => {
  // TODO: Implement contact form submission
  alert('Thank you for your message!')
}
</script>
