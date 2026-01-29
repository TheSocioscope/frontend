<template>
  <section class="newsletter">
    <div class="container">
      <div class="newsletter-content">
        <h2>{{ $t('newsletter.title') }}</h2>
        <form class="newsletter-form" @submit.prevent="handleSubmit">
          <div class="input-wrapper">
            <input
              v-model="email"
              type="email"
              :placeholder="$t('newsletter.emailPlaceholder')"
              :class="{ invalid: emailError }"
              required
              @blur="validateEmail"
              @input="emailError = ''"
            />
            <span v-if="emailError" class="error-message">{{ emailError }}</span>
          </div>
          <button type="submit" :disabled="!isValidEmail">{{ $t('newsletter.button') }}</button>
        </form>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const email = ref('')
const emailError = ref('')

const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/

const isValidEmail = computed(() => emailRegex.test(email.value))

const validateEmail = () => {
  if (!email.value) {
    emailError.value = $t('newsletter.emailRequired')
  } else if (!isValidEmail.value) {
    emailError.value = $t('newsletter.emailInvalid')
  } else {
    emailError.value = ''
  }
}

const handleSubmit = () => {
  validateEmail()
  if (email.value && isValidEmail.value) {
    // TODO: Implement newsletter subscription logic
    alert($t('newsletter.success'))
    email.value = ''
  }
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.newsletter {
  padding: 5rem 0;
  background: $green-bright;
  color: $cream;
}

.newsletter-content {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;

  h2 {
    font-family: $font-family-display;
    font-size: clamp(1.5rem, 3vw, 2rem);
    font-weight: $font-weight-bold;
    margin-bottom: 1rem;
    color: $cream;
  }
}

.newsletter-form {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  justify-content: center;
  align-items: flex-start;

  @media (max-width: 768px) {
    flex-direction: column;
  }

  .input-wrapper {
    flex: 1;
    max-width: 400px;
    position: relative;

    @media (max-width: 768px) {
      max-width: 100%;
      width: 100%;
    }
  }

  input {
    padding: 1rem 1.5rem;
    border: 2px solid transparent;
    border-radius: 4px;
    font-size: 1rem;
    font-family: $font-family-base;
    width: 100%;
    background: white;
    transition: border-color 0.3s;

    &::placeholder {
      color: #666;
    }

    &.invalid {
      border-color: #e74c3c;
    }
  }

  .error-message {
    display: block;
    color: #ffcccc;
    font-size: 0.85rem;
    margin-top: 0.5rem;
    text-align: left;
  }

  button {
    padding: 1rem 2.5rem;
    background: $forest-green;
    color: white;
    border: none;
    border-radius: 4px;
    font-family: $font-family-base;
    font-weight: $font-weight-semibold;
    cursor: pointer;
    transition: background 0.3s;

    &:hover {
      background: $brown-dark;
    }

    @media (max-width: 768px) {
      width: 100%;
    }
  }
}
</style>
