<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="isOpen" class="drawer-overlay" @click="handleClose">
        <div class="drawer-panel" role="dialog" aria-label="Connect with initiative" @click.stop>
          <!-- Header -->
          <div class="drawer-header">
            <div class="drawer-header-text">
              <p class="drawer-label">Connect</p>
              <h2 class="drawer-title">{{ localizedName }}</h2>
            </div>
            <button class="close-btn" aria-label="Close" @click="handleClose">&times;</button>
          </div>

          <!-- Body -->
          <div class="drawer-body">
            <p class="drawer-intro">
              Want to connect with this initiative? Fill in your details and tell us why — we'll
              forward your message on their behalf.
            </p>

            <div class="form-group">
              <label>Your name *</label>
              <input v-model="form.name" type="text" placeholder="Jane Smith" />
              <p v-if="showValidation && !form.name.trim()" class="validation-error">
                Please enter your name.
              </p>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>Email</label>
                <input v-model="form.email" type="email" placeholder="you@example.com" />
              </div>
              <div class="form-group">
                <label>Phone</label>
                <input v-model="form.phone" type="tel" placeholder="+1 234 567 8900" />
              </div>
            </div>
            <p v-if="showValidation && !isContactValid" class="validation-error">
              Please provide at least an email or phone number.
            </p>

            <div class="form-group">
              <label>Reason for connection *</label>
              <textarea
                v-model="form.reason"
                rows="5"
                placeholder="Describe why you'd like to connect and what you're hoping to explore together…"
                class="edit-textarea"
              />
              <p v-if="showValidation && !form.reason.trim()" class="validation-error">
                Please describe your reason for connecting.
              </p>
            </div>
          </div>

          <!-- Footer -->
          <div class="drawer-footer">
            <Transition name="fade">
              <div v-if="submitted" class="success-message">
                ✓ Message sent — we'll be in touch soon.
              </div>
              <div v-else-if="submitError" class="error-message">{{ submitError }}</div>
              <button
                v-else
                type="button"
                class="submit-btn"
                :disabled="submitting"
                @click="handleSubmit"
              >
                {{ submitting ? 'Sending…' : 'Send message' }}
              </button>
            </Transition>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { web3formsKey } from '~~/static.config'

const props = defineProps<{
  isOpen: boolean
  project: any
  localizedName: string
  pageUrl: string
}>()

const emit = defineEmits<{ close: [] }>()

const form = ref({ name: '', email: '', phone: '', reason: '' })
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
const showValidation = ref(false)

const isContactValid = computed(() => form.value.email.trim() || form.value.phone.trim())
const isValid = computed(
  () =>
    form.value.name.trim() &&
    isContactValid.value &&
    form.value.reason.trim()
)

watch(
  () => props.isOpen,
  (open) => {
    if (open) {
      form.value = { name: '', email: '', phone: '', reason: '' }
      submitted.value = false
      submitError.value = ''
      showValidation.value = false
    }
  }
)

const buildEmailBody = (): string => {
  const proj = props.project as any
  const lines: string[] = []
  lines.push(`Initiative: ${props.localizedName} (#${proj?.pubId ?? ''})`)
  lines.push(`Page: ${props.pageUrl}`)
  lines.push('')
  lines.push(`From: ${form.value.name}`)
  if (form.value.email) lines.push(`Email: ${form.value.email}`)
  if (form.value.phone) lines.push(`Phone: ${form.value.phone}`)
  lines.push('')
  lines.push('--- REASON FOR CONNECTION ---')
  lines.push(form.value.reason.trim())
  return lines.join('\n')
}

const handleSubmit = async () => {
  showValidation.value = true
  if (!isValid.value) return

  submitting.value = true
  submitError.value = ''

  try {
    const proj = props.project as any
    const res = await fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        access_key: web3formsKey,
        subject: `Connection request — ${props.localizedName} (#${proj?.pubId ?? ''})`,
        from_name: form.value.name,
        email: form.value.email || 'noreply@thesocioscope.org',
        replyto: form.value.email || '',
        message: buildEmailBody(),
      }),
    })
    const data = await res.json()
    if (data.success) {
      submitted.value = true
    } else {
      submitError.value = 'Something went wrong. Please try again.'
    }
  } catch {
    submitError.value = 'Something went wrong. Please try again.'
  } finally {
    submitting.value = false
  }
}

const handleClose = () => emit('close')
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.drawer-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  z-index: $z-modal;
  display: flex;
  justify-content: flex-end;
}

.drawer-panel {
  width: 480px;
  max-width: 100vw;
  height: 100%;
  background: $cream;
  display: flex;
  flex-direction: column;
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.15);
  overflow: hidden;

  @media (max-width: 600px) {
    width: 100vw;
  }
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 2px solid $border-cream;
  background: #2c6e49;
  color: white;
  flex-shrink: 0;
}

.drawer-header-text {
  flex: 1;
  min-width: 0;
}

.drawer-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  opacity: 0.75;
  margin: 0 0 0.25rem;
}

.drawer-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.close-btn {
  background: none;
  border: none;
  color: white;
  font-size: 1.75rem;
  line-height: 1;
  cursor: pointer;
  padding: 0 0 0 1rem;
  opacity: 0.8;
  flex-shrink: 0;
  transition: opacity $transition-fast;

  &:hover {
    opacity: 1;
  }
}

.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.drawer-intro {
  color: $brown-medium;
  font-size: 0.9rem;
  line-height: 1.55;
  margin: 0 0 1.5rem;
  padding: 0.85rem 1rem;
  background: $cream-dark;
  border-radius: $border-radius-md;
}

.form-group {
  margin-bottom: 1.1rem;

  label {
    display: block;
    font-size: 0.8rem;
    font-weight: 600;
    color: $brown-dark;
    margin-bottom: 0.3rem;
  }

  input {
    width: 100%;
    padding: 0.6rem 0.75rem;
    border: 1.5px solid $border-cream;
    border-radius: $border-radius-md;
    font-size: 0.9rem;
    font-family: $font-family-base;
    background: white;
    color: $brown-dark;
    transition: border-color $transition-fast;
    box-sizing: border-box;

    &:focus {
      outline: none;
      border-color: #2c6e49;
    }
  }
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.75rem;

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
}

.edit-textarea {
  width: 100%;
  padding: 0.6rem 0.75rem;
  border: 1.5px solid $border-cream;
  border-radius: $border-radius-md;
  font-size: 0.9rem;
  font-family: $font-family-base;
  background: white;
  color: $brown-dark;
  resize: vertical;
  min-height: 100px;
  box-sizing: border-box;
  transition: border-color $transition-fast;

  &:focus {
    outline: none;
    border-color: #2c6e49;
  }
}

.validation-error {
  font-size: 0.82rem;
  color: #e53935;
  margin: 0.3rem 0 0;
}

.drawer-footer {
  padding: 1rem 1.5rem;
  border-top: 2px solid $border-cream;
  background: $cream;
  flex-shrink: 0;
}

.submit-btn {
  width: 100%;
  background: #2c6e49;
  color: white;
  border: none;
  padding: 0.875rem;
  font-size: 1rem;
  font-weight: 700;
  font-family: $font-family-base;
  border-radius: $border-radius-md;
  cursor: pointer;
  transition: all $transition-base;

  &:hover:not(:disabled) {
    background: $green-bright;
    transform: translateY(-1px);
    box-shadow: $shadow-md;
  }

  &:disabled {
    opacity: 0.55;
    cursor: not-allowed;
  }
}

.success-message {
  text-align: center;
  font-weight: 600;
  color: #2c6e49;
  font-size: 0.95rem;
  padding: 0.5rem 0;
}

.error-message {
  text-align: center;
  color: #e53935;
  font-size: 0.88rem;
  padding: 0.5rem 0;
}

.drawer-enter-active,
.drawer-leave-active {
  transition: opacity $transition-base;

  .drawer-panel {
    transition: transform $transition-base;
  }
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;

  .drawer-panel {
    transform: translateX(100%);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity $transition-fast;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
