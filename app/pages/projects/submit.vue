<template>
  <v-container class="py-12">
    <v-row justify="center">
      <v-col cols="12" class="text-center mb-8">
        <h1 class="text-h2 mb-4">{{ $t('projects.submit.title') }}</h1>
        <p class="text-h6">{{ $t('projects.submit.subtitle') }}</p>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="12" md="10" lg="8">
        <v-card class="form-container" elevation="0">
          <v-card-text>
            <v-form ref="form" @submit.prevent="handleSubmit">
              <v-text-field
                v-model="formData.name"
                :label="$t('projects.submit.name')"
                :rules="[rules.required]"
                variant="outlined"
                class="mb-4"
              />

              <v-text-field
                v-model="formData.location"
                :label="$t('projects.submit.location')"
                :rules="[rules.required]"
                variant="outlined"
                class="mb-4"
              />

              <v-textarea
                v-model="formData.description"
                :label="$t('projects.submit.description')"
                :rules="[rules.required]"
                variant="outlined"
                rows="5"
                class="mb-4"
              />

              <v-text-field
                v-model="formData.email"
                :label="$t('projects.submit.email')"
                :rules="[rules.required, rules.email]"
                type="email"
                variant="outlined"
                class="mb-6"
              />

              <v-btn
                type="submit"
                color="green-bright"
                size="large"
                rounded="pill"
                block
                :loading="loading"
              >
                {{ $t('projects.submit.button') }}
              </v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const { t } = useI18n()

useHead({
  title: t('projects.submit.title')
})

const form = ref()
const loading = ref(false)
const formData = reactive({
  name: '',
  location: '',
  description: '',
  email: ''
})

const rules = {
  required: (v: string) => !!v || t('common.required'),
  email: (v: string) => /.+@.+\..+/.test(v) || t('common.emailInvalid')
}

const handleSubmit = async () => {
  const { valid } = await form.value.validate()
  if (!valid) return

  loading.value = true
  
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    alert(t('projects.submit.success'))
    formData.name = ''
    formData.location = ''
    formData.description = ''
    formData.email = ''
    form.value.reset()
  } catch (error) {
    alert(t('common.error'))
  } finally {
    loading.value = false
  }
}
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.form-container {
  background: white;
  border: 2px solid $border-cream;
  border-radius: $border-radius-lg;
  padding: $spacing-2xl;
}
</style>
