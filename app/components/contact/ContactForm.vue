<template>
  <section class="section">
    <div class="container">
      <div class="contact-grid">
        <!-- Contact Form -->
        <div class="form-section">
          <h2>{{ $t('contact.form.title') }}</h2>

          <div v-if="showSuccessMessage" class="success-message">
            ✓ {{ $t('contact.form.successMessage') }}
          </div>

          <form class="contact-form" @submit.prevent="handleSubmit">
            <div class="form-group">
              <label for="name">{{ $t('contact.form.name') }} *</label>
              <input
                id="name"
                v-model="formData.name"
                type="text"
                required
                :placeholder="$t('contact.form.namePlaceholder')"
              />
            </div>

            <div class="form-group">
              <label for="email">{{ $t('contact.form.email') }} *</label>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                :placeholder="$t('contact.form.emailPlaceholder')"
              />
            </div>

            <div class="form-group">
              <label for="subject">{{ $t('contact.form.subject') }} *</label>
              <input
                id="subject"
                v-model="formData.subject"
                type="text"
                required
                :placeholder="$t('contact.form.subjectPlaceholder')"
              />
            </div>

            <div class="form-group">
              <label for="message">{{ $t('contact.form.message') }} *</label>
              <textarea
                id="message"
                v-model="formData.message"
                required
                :placeholder="$t('contact.form.messagePlaceholder')"
              />
            </div>

            <button type="submit" class="btn" :disabled="isSubmitting">
              {{ isSubmitting ? $t('contact.form.sending') : $t('contact.form.submit') }}
            </button>
          </form>
        </div>

        <!-- Contact Info Sidebar -->
        <ContactInfo />
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const formData = ref({
  name: '',
  email: '',
  subject: '',
  message: ''
})

const isSubmitting = ref(false)
const showSuccessMessage = ref(false)

const handleSubmit = async () => {
  isSubmitting.value = true

  // Simulate sending (in production, this would be an API call)
  await new Promise((resolve) => setTimeout(resolve, 1500))

  // Show success message
  showSuccessMessage.value = true

  // Reset form
  formData.value = {
    name: '',
    email: '',
    subject: '',
    message: ''
  }

  // Reset button
  isSubmitting.value = false

  // Hide success message after 5 seconds
  setTimeout(() => {
    showSuccessMessage.value = false
  }, 5000)

  // Scroll to success message
  const successEl = document.querySelector('.success-message')
  if (successEl) {
    successEl.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
  }
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.section {
  padding: 5rem 0;
  background: $cream;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.contact-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 4rem;
}

.form-section h2 {
  margin-bottom: 2rem;
  font-size: 2.5rem;
  font-family: 'Playfair Display', serif;
  font-weight: 700;
}

.contact-form {
  background: white;
  padding: 2.5rem;
  border: 2px solid $warm-beige;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  font-weight: 600;
  margin-bottom: 0.5rem;
  font-size: 1.05rem;
}

input,
textarea {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
  font-family: 'Playfair Display', serif;
  border: 2px solid $warm-beige;
  background: white;
  color: $brown-dark;
  transition: all 0.3s;

  &:focus {
    outline: none;
    border-color: $green-bright;
  }
}

textarea {
  resize: vertical;
  min-height: 150px;
}

.btn {
  width: 100%;
  padding: 1.25rem 2rem;
  background: $green-bright;
  color: white;
  border: none;
  font-size: 1rem;
  font-weight: 600;
  font-family: 'Playfair Display', serif;
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    background: $forest-green;
  }

  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
}

.success-message {
  background: $green-bright;
  color: white;
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  animation: slideIn 0.5s ease;
  text-align: center;
  font-weight: 600;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 1024px) {
  .contact-grid {
    grid-template-columns: 1fr;
    gap: 3rem;
  }
}

@media (max-width: 768px) {
  .section {
    padding: 4rem 0;
  }

  .contact-form {
    padding: 1.5rem;
  }
}
</style>
