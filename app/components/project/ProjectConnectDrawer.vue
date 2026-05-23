<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="isOpen" class="drawer-overlay" @click="handleClose">
        <div class="drawer-panel" role="dialog" aria-label="Connect with initiative" @click.stop>
          <!-- Header — initiative-aware so the user knows whose page they
               came from. Avatar + name in Playfair + location + close. -->
          <header class="drawer-header">
            <div class="header-top">
              <span class="header-eyebrow">{{ $t('projects.detail.connect', 'Connect') }}</span>
              <button class="close-btn" :aria-label="$t('common.close', 'Close')" @click="handleClose">
                <v-icon>mdi-close</v-icon>
              </button>
            </div>
            <div class="header-id">
              <span class="initiative-avatar" :style="{ background: avatarBg }">
                {{ avatarInitials }}
              </span>
              <div class="initiative-meta">
                <h2 class="initiative-name">{{ localizedName }}</h2>
                <p v-if="project?.location" class="initiative-location">
                  <v-icon size="x-small">mdi-map-marker</v-icon>
                  {{ project.location }}
                </p>
              </div>
            </div>
            <div v-if="factChips.length" class="header-chips">
              <span v-for="(chip, i) in factChips" :key="i" class="header-chip">
                {{ chip }}
              </span>
            </div>
          </header>

          <!-- Body -->
          <div class="drawer-body">
            <p class="drawer-intro">
              <v-icon size="small" class="intro-icon">mdi-information-outline</v-icon>
              <span>
                {{
                  $t(
                    'projects.detail.connectIntro',
                    "We'll forward your message to the team — they'll respond directly."
                  )
                }}
              </span>
            </p>

            <div class="form-group">
              <label>{{ $t('projects.detail.connectName', 'Your name') }} *</label>
              <input v-model="form.name" type="text" placeholder="Jane Smith" />
              <p v-if="showValidation && !form.name.trim()" class="validation-error">
                {{ $t('projects.detail.connectNameError', 'Please enter your name.') }}
              </p>
            </div>

            <div class="form-row">
              <div class="form-group">
                <label>{{ $t('projects.detail.connectEmail', 'Email') }}</label>
                <input v-model="form.email" type="email" placeholder="you@example.com" />
              </div>
              <div class="form-group">
                <label>{{ $t('projects.detail.connectPhone', 'Phone') }}</label>
                <input v-model="form.phone" type="tel" placeholder="+1 234 567 8900" />
              </div>
            </div>
            <p v-if="showValidation && !isContactValid" class="validation-error">
              {{
                $t(
                  'projects.detail.connectContactError',
                  'Please provide at least an email or phone number.'
                )
              }}
            </p>

            <div class="form-group">
              <label>{{ $t('projects.detail.connectReason', 'Why do you want to connect?') }} *</label>
              <textarea
                v-model="form.reason"
                rows="3"
                :placeholder="
                  $t(
                    'projects.detail.connectReasonPlaceholder',
                    'A short message — what you do, what you hope to explore together…'
                  )
                "
                class="edit-textarea"
              />
              <p v-if="showValidation && !form.reason.trim()" class="validation-error">
                {{
                  $t(
                    'projects.detail.connectReasonError',
                    'Please describe your reason for connecting.'
                  )
                }}
              </p>
            </div>
          </div>

          <!-- Footer -->
          <div class="drawer-footer">
            <Transition name="fade">
              <div v-if="submitted" class="success-message">
                <v-icon color="success">mdi-check-circle</v-icon>
                {{
                  $t(
                    'projects.detail.connectSuccess',
                    "Message sent — we'll be in touch soon."
                  )
                }}
              </div>
              <div v-else-if="submitError" class="error-message">{{ submitError }}</div>
              <button
                v-else
                type="button"
                class="submit-btn"
                :disabled="submitting"
                @click="handleSubmit"
              >
                <v-icon size="small">mdi-send-outline</v-icon>
                {{
                  submitting
                    ? $t('projects.detail.connectSending', 'Sending…')
                    : $t('projects.detail.connectSend', 'Send to ' + (localizedName || 'team'))
                }}
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

const { t: $t } = useI18n()
const { getContinentLabel, getCountryLabel } = useProjectMappings()

const form = ref({ name: '', email: '', phone: '', reason: '' })
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
const showValidation = ref(false)

const isContactValid = computed(() => form.value.email.trim() || form.value.phone.trim())
const isValid = computed(
  () => form.value.name.trim() && isContactValid.value && form.value.reason.trim()
)

const avatarInitials = computed(() => {
  const words = (props.localizedName || '').trim().split(/\s+/)
  return words.length >= 2
    ? (words[0][0] + words[1][0]).toUpperCase()
    : (props.localizedName || '?').slice(0, 2).toUpperCase()
})

const avatarBg = computed(() => {
  const colors = ['#27421d', '#4ca049', '#5c4a2f', '#6b8e23', '#8b6f47']
  const id = (props.project as any)?.pubId ?? 0
  return colors[id % colors.length]
})

// Three small chips reinforcing what initiative the user is connecting
// with — first continent, first country, first sector. Empty values
// are skipped; cap at 3 to avoid clutter.
const factChips = computed<string[]>(() => {
  const p = props.project as any
  if (!p) return []
  const chips: string[] = []
  const continent = (p.continent || [])[0]
  const country = (p.country || [])[0]
  const sector = (p.sectorFocus || [])[0]
  if (continent) chips.push(getContinentLabel(continent))
  if (country) chips.push(getCountryLabel(country))
  if (sector) chips.push(sector)
  return chips.slice(0, 3)
})

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
        message: buildEmailBody()
      })
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
  background: rgba(44, 36, 22, 0.45);
  z-index: $z-modal;
  display: flex;
  /* Right rail on desktop; bottom sheet on mobile (see media below) */
  justify-content: flex-end;
  align-items: stretch;
}

.drawer-panel {
  width: 460px;
  max-width: 100vw;
  /* dvh accounts for mobile browser chrome (URL bar, bottom bar) so
     the footer stays visible. Fallback to vh for older browsers. */
  height: 100vh;
  height: 100dvh;
  background: $surface-page;
  display: flex;
  flex-direction: column;
  box-shadow: -4px 0 32px rgba(0, 0, 0, 0.18);
  overflow: hidden;
}

/* Mobile: floating center modal — card sized to content (capped at
   92dvh) so the form fits without internal scrolling. */
@media (max-width: 600px) {
  .drawer-overlay {
    justify-content: center;
    align-items: center;
    padding: 12px;
  }

  .drawer-panel {
    width: 100%;
    max-width: 480px;
    height: auto;
    max-height: 92dvh;
    border-radius: 14px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.22);
  }
}

/* ----------------------------- Header ----------------------------- */
.drawer-header {
  background: $earth-5;
  border-bottom: 1px solid $border-soft;
  padding: 18px 24px 16px;
  flex-shrink: 0;

  @media (max-width: 600px) {
    /* Tighter on phone so the body fits without scroll */
    padding: 12px 16px;
    border-top-left-radius: 14px;
    border-top-right-radius: 14px;
  }
}

.header-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;

  @media (max-width: 600px) {
    margin-bottom: 8px;
  }
}

.header-eyebrow {
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: $green-leaf;
}

.close-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  color: $green-forest;
  cursor: pointer;
  transition: background 0.15s;

  &:hover {
    background: $earth-15;
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }
}

.header-id {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 12px;

  @media (max-width: 600px) {
    gap: 10px;
    margin-bottom: 8px;
  }
}

.initiative-avatar {
  @media (max-width: 600px) {
    width: 40px;
    height: 40px;
    font-size: 0.875rem;
  }
}

.initiative-name {
  @media (max-width: 600px) {
    font-size: 1.0625rem;
  }
}

.initiative-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.initiative-meta {
  flex: 1;
  min-width: 0;
}

.initiative-name {
  margin: 0 0 2px;
  font-family: $font-family-display;
  font-size: 1.25rem;
  font-weight: 700;
  color: $green-forest;
  line-height: 1.2;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  word-break: break-word;
}

.initiative-location {
  margin: 0;
  font-size: 0.8125rem;
  color: $text-caption;
  display: inline-flex;
  align-items: center;
  gap: 2px;
}

.header-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.header-chip {
  background: white;
  border: 1px solid $border-soft;
  color: $text-secondary;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  white-space: nowrap;
}

/* ----------------------------- Body ------------------------------- */
.drawer-body {
  flex: 1;
  overflow-y: auto;
  padding: 20px 24px 24px;

  @media (max-width: 600px) {
    /* Tight padding + non-scrolling: with reduced fields the body now
       fits comfortably inside the 92dvh cap without an inner scroll. */
    padding: 12px 16px 14px;
    overflow-y: visible;
  }
}

.drawer-intro {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  font-size: 0.875rem;
  line-height: 1.5;
  color: $text-secondary;
  margin: 0 0 18px;
  padding: 0;
  background: transparent;
  border: none;

  @media (max-width: 600px) {
    font-size: 0.8125rem;
    line-height: 1.4;
    margin-bottom: 12px;
  }
}

.intro-icon {
  color: $green-leaf;
  flex-shrink: 0;
  margin-top: 1px;
}

.form-group {
  margin-bottom: 14px;

  @media (max-width: 600px) {
    margin-bottom: 10px;
  }

  label {
    display: block;
    font-size: 0.6875rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: $text-caption;
    margin-bottom: 6px;
  }

  input {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid $border-soft;
    border-radius: 6px;
    font-size: 0.9375rem;
    font-family: $font-family-base;
    background: white;
    color: $text-primary;
    transition:
      border-color 0.15s,
      box-shadow 0.15s;
    box-sizing: border-box;

    @media (max-width: 600px) {
      padding: 8px 10px;
      font-size: 0.875rem;
    }

    &::placeholder {
      color: $text-disabled;
    }

    &:focus {
      outline: none;
      border-color: $green-leaf;
      box-shadow: 0 0 0 3px rgba(76, 160, 73, 0.15);
    }
  }
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
    gap: 0;
  }
}

.edit-textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid $border-soft;
  border-radius: 6px;
  font-size: 0.9375rem;
  font-family: $font-family-base;
  background: white;
  color: $text-primary;
  resize: vertical;
  min-height: 110px;
  box-sizing: border-box;
  line-height: 1.5;
  transition:
    border-color 0.15s,
    box-shadow 0.15s;

  @media (max-width: 600px) {
    padding: 8px 10px;
    font-size: 0.875rem;
    min-height: 70px;
    line-height: 1.45;
  }

  &::placeholder {
    color: $text-disabled;
  }

  &:focus {
    outline: none;
    border-color: $green-leaf;
    box-shadow: 0 0 0 3px rgba(76, 160, 73, 0.15);
  }
}

.validation-error {
  font-size: 0.75rem;
  color: #c0392b;
  margin: 4px 0 0;
}

/* ----------------------------- Footer ----------------------------- */
.drawer-footer {
  padding: 14px 24px 18px;
  border-top: 1px solid $border-soft;
  background: $surface-page;
  flex-shrink: 0;

  @media (max-width: 600px) {
    padding: 10px 16px 12px;
  }
}

.submit-btn {
  width: 100%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: $green-leaf;
  color: white;
  border: none;
  padding: 12px;
  font-size: 0.9375rem;
  font-weight: 600;
  font-family: $font-family-base;
  border-radius: 6px;
  cursor: pointer;
  transition:
    background 0.15s,
    transform 0.15s,
    box-shadow 0.15s;

  &:hover:not(:disabled) {
    background: $green-leaf-dark;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(76, 160, 73, 0.2);
  }

  &:focus-visible {
    outline: 2px solid $green-forest;
    outline-offset: 2px;
  }

  &:disabled {
    opacity: 0.55;
    cursor: not-allowed;
  }
}

.success-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  text-align: center;
  font-weight: 600;
  color: $green-forest;
  font-size: 0.9375rem;
  padding: 6px 0;
}

.error-message {
  text-align: center;
  color: #c0392b;
  font-size: 0.875rem;
  padding: 6px 0;
}

/* ---------------------------- Transitions ------------------------- */
.drawer-enter-active,
.drawer-leave-active {
  transition: opacity 0.25s;

  .drawer-panel {
    transition: transform 0.25s;
  }
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;

  .drawer-panel {
    /* Desktop: slide from the right edge */
    transform: translateX(100%);
  }

  /* Mobile: floating modal scales up gently from 96% */
  @media (max-width: 600px) {
    .drawer-panel {
      transform: scale(0.96);
    }
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (prefers-reduced-motion: reduce) {
  .drawer-enter-active,
  .drawer-leave-active,
  .drawer-enter-active .drawer-panel,
  .drawer-leave-active .drawer-panel,
  .submit-btn,
  .submit-btn:hover {
    transition: none !important;
    transform: none !important;
  }
}
</style>
