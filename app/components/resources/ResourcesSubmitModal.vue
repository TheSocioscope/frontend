<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="handleClose">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h2>{{ $t('resources.modal.title') }}</h2>
            <button class="close-btn" @click="handleClose">&times;</button>
          </div>

          <div class="modal-body">
            <div v-if="submitted" class="success-message">
              ✓ {{ $t('resources.modal.successMessage') }}
            </div>

            <form v-else class="submission-form" @submit.prevent="handleSubmit">
              <h3 class="form-section-title">{{ $t('resources.modal.resourceInfo') }}</h3>
              <p class="form-section-subtitle">{{ $t('resources.modal.resourceInfoSubtitle') }}</p>

              <div class="form-group">
                <label>{{ $t('resources.modal.fields.type') }} *</label>
                <select v-model="formData.type" required>
                  <option value="">{{ $t('resources.modal.fields.selectType') }}</option>
                  <option value="article">{{ $t('resources.categoryLabels.article') }}</option>
                  <option value="book">{{ $t('resources.categoryLabels.book') }}</option>
                  <option value="event">{{ $t('resources.categoryLabels.event') }}</option>
                  <option value="funding">{{ $t('resources.categoryLabels.funding') }}</option>
                  <option value="organization">
                    {{ $t('resources.categoryLabels.organization') }}
                  </option>
                  <option value="policy">{{ $t('resources.categoryLabels.policy') }}</option>
                </select>
              </div>

              <div class="form-group">
                <label>{{ $t('resources.modal.fields.title') }} *</label>
                <input v-model="formData.title" type="text" required />
              </div>

              <div class="form-group">
                <label>{{ $t('resources.modal.fields.authors') }}</label>
                <input v-model="formData.authors" type="text" />
              </div>

              <div class="form-group">
                <label>{{ $t('resources.modal.fields.description') }} *</label>
                <textarea v-model="formData.description" rows="4" required />
              </div>

              <div class="form-group">
                <label>{{ $t('resources.modal.fields.url') }} *</label>
                <input v-model="formData.url" type="url" required />
              </div>

              <h3 class="form-section-title">{{ $t('resources.modal.yourInfo') }}</h3>
              <p class="form-section-subtitle">{{ $t('resources.modal.yourInfoSubtitle') }}</p>

              <div class="form-row">
                <div class="form-group">
                  <label>{{ $t('resources.modal.fields.yourName') }} *</label>
                  <input v-model="formData.submitterName" type="text" required />
                </div>

                <div class="form-group">
                  <label>{{ $t('resources.modal.fields.yourEmail') }} *</label>
                  <input v-model="formData.submitterEmail" type="email" required />
                </div>
              </div>

              <button type="submit" class="submit-btn">
                {{ $t('resources.modal.submitButton') }}
              </button>
            </form>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
const { t } = useI18n()

const props = defineProps<{
  isOpen: boolean
}>()

const emit = defineEmits<{
  close: []
}>()

const submitted = ref(false)
const formData = ref({
  type: '',
  title: '',
  authors: '',
  description: '',
  url: '',
  submitterName: '',
  submitterEmail: ''
})

const handleClose = () => {
  emit('close')
  setTimeout(() => {
    submitted.value = false
    formData.value = {
      type: '',
      title: '',
      authors: '',
      description: '',
      url: '',
      submitterName: '',
      submitterEmail: ''
    }
  }, 300)
}

const handleSubmit = () => {
  // In a real app, send to backend
  console.log('Submitting resource:', formData.value)
  submitted.value = true

  setTimeout(() => {
    handleClose()
  }, 3000)
}
</script>

<style scoped lang="scss">
@use 'sass:color';
@use '../../../assets/styles/variables' as *;

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: $border-radius-lg;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2rem;
  border-bottom: 2px solid $border-cream;

  h2 {
    font-family: $font-family-display;
    font-size: 2rem;
    color: $brown-dark;
    margin: 0;
  }
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: $brown-dark;
  cursor: pointer;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;

  &:hover {
    opacity: 0.6;
  }
}

.modal-body {
  padding: 2rem;
}

.success-message {
  background: color.adjust($green-bright, $lightness: 45%);
  color: color.adjust($green-bright, $lightness: -20%);
  padding: 1.5rem;
  border-radius: $border-radius-lg;
  text-align: center;
  font-size: 1.1rem;
  font-weight: 600;
}

.submission-form {
  .form-section-title {
    font-family: $font-family-display;
    font-size: 1.5rem;
    color: $brown-dark;
    margin: 2rem 0 0.5rem;

    &:first-child {
      margin-top: 0;
    }
  }

  .form-section-subtitle {
    color: $brown-dark;
    opacity: 0.7;
    margin-bottom: 1.5rem;
  }

  .form-group {
    margin-bottom: 1.5rem;

    label {
      display: block;
      font-weight: 600;
      color: $brown-dark;
      margin-bottom: 0.5rem;
    }

    input,
    select,
    textarea {
      width: 100%;
      padding: 0.75rem;
      border: 2px solid $border-cream;
      border-radius: $border-radius-lg;
      font-size: 1rem;
      font-family: inherit;
      transition: all 0.3s ease;

      &:focus {
        outline: none;
        border-color: $green-bright;
      }
    }

    textarea {
      resize: vertical;
    }
  }

  .form-row {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;

    @media (max-width: 768px) {
      grid-template-columns: 1fr;
    }
  }

  .submit-btn {
    width: 100%;
    background: $green-bright;
    color: white;
    padding: 1rem;
    font-size: 1.1rem;
    font-weight: 600;
    border: none;
    border-radius: 0;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 1rem;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
  }
}

.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>
