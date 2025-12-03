<template>
  <section class="newsletter-section gradient-green">
    <v-container>
      <div class="newsletter-content">
        <h2 class="text-h3 text-md-h2 font-weight-medium mb-4 white--text">
          {{ $t('newsletter.title') }}
        </h2>
        <p class="text-body-1 newsletter-subtitle">
          {{ $t('newsletter.subtitle') }}
        </p>

        <v-form v-model="valid" class="newsletter-form" @submit.prevent="handleSubmit">
          <v-text-field
            v-model="email"
            :placeholder="$t('newsletter.emailPlaceholder')"
            :rules="emailRules"
            type="email"
            variant="outlined"
            bg-color="rgba(255, 255, 255, 0.1)"
            class="newsletter-input"
            required
          />

          <v-btn
            type="submit"
            color="accent"
            size="large"
            :disabled="!valid"
            class="newsletter-button"
          >
            {{ $t('newsletter.button') }}
          </v-btn>
        </v-form>
      </div>
    </v-container>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const email = ref('')
const valid = ref(false)

const emailRules = [
  (v: string) => !!v || 'Email is required',
  (v: string) => /.+@.+\..+/.test(v) || 'Email must be valid'
]

const handleSubmit = () => {
  if (valid.value) {
    // TODO: Implement newsletter subscription logic
    alert($t('newsletter.title'))
    email.value = ''
  }
}
</script>

<style scoped lang="scss">
@use '../../assets/styles/variables' as *;

.newsletter-section {
  padding: $spacing-3xl 0;
  color: white;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255, 255, 255, 0.05) 0%, transparent 70%);
    top: -100%;
    left: -50%;
    animation: shimmer 15s ease-in-out infinite;
  }
}

.newsletter-content {
  text-align: center;
  position: relative;
  z-index: 1;
  max-width: 800px;
  margin: 0 auto;
}

.newsletter-subtitle {
  margin-bottom: $spacing-xl;
  opacity: 0.95;
  line-height: 1.7;
}

.newsletter-form {
  display: flex;
  gap: $spacing-md;
  max-width: 600px;
  margin: 0 auto;
  align-items: stretch;

  @media (max-width: 768px) {
    flex-direction: column;
  }
}

.newsletter-input {
  flex: 1;

  :deep(.v-field) {
    border: 2px solid rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(10px);
    height: 56px;
  }

  :deep(.v-field__input) {
    color: white;
  }

  :deep(.v-field__input::placeholder) {
    color: rgba(255, 255, 255, 0.7);
  }
}

.newsletter-button {
  height: 56px;

  @media (max-width: 768px) {
    width: 100%;
  }
}
</style>
