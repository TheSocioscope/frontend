<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div v-if="isOpen" class="drawer-overlay" @click="handleClose">
        <div class="drawer-panel" role="dialog" :aria-label="$t('editDrawer.title')" @click.stop>
          <!-- Header -->
          <div class="drawer-header">
            <div class="drawer-header-text">
              <p class="drawer-label">{{ $t('editDrawer.label') }}</p>
              <h2 class="drawer-title">{{ localizedName }}</h2>
            </div>
            <button class="close-btn" :aria-label="$t('editDrawer.close')" @click="handleClose">
              &times;
            </button>
          </div>

          <!-- Body -->
          <div class="drawer-body">
            <p class="drawer-intro">{{ $t('editDrawer.intro') }}</p>

            <!-- Contact details -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.yourDetails') }}</h3>
              <div class="form-group">
                <label>{{ $t('editDrawer.name') }} *</label>
                <input v-model="contact.name" type="text" :placeholder="$t('editDrawer.namePlaceholder')" />
              </div>
              <div class="form-row">
                <div class="form-group">
                  <label>{{ $t('editDrawer.email') }}</label>
                  <input v-model="contact.email" type="email" placeholder="you@example.com" />
                </div>
                <div class="form-group">
                  <label>{{ $t('editDrawer.phone') }}</label>
                  <input v-model="contact.phone" type="tel" placeholder="+1 234 567 8900" />
                </div>
              </div>
              <p class="field-hint">{{ $t('editDrawer.contactHint') }}</p>
              <p v-if="showValidation && !isContactValid" class="validation-error">
                {{ $t('editDrawer.validationContact') }}
              </p>
            </section>

            <div class="section-divider" />

            <!-- Description -->
            <section class="edit-section">
              <div class="section-header-row">
                <h3 class="section-title">{{ $t('editDrawer.description') }}</h3>
                <span v-if="isChanged('description')" class="changed-badge">{{ $t('editDrawer.modified') }}</span>
              </div>
              <textarea v-model="edits.description" rows="6" class="edit-textarea" />
            </section>

            <div class="section-divider" />

            <!-- Timeline -->
            <section v-if="timelineEdits.length" class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.timeline') }}</h3>
              <div v-for="(entry, i) in timelineEdits" :key="i" class="list-entry">
                <div class="entry-header-row">
                  <label class="entry-label">{{ entry.date || '—' }}</label>
                  <span v-if="entry.current !== entry.original" class="changed-badge">
                    {{ $t('editDrawer.modified') }}
                  </span>
                </div>
                <textarea v-model="entry.current" rows="3" class="edit-textarea" />
              </div>
            </section>

            <div v-if="timelineEdits.length" class="section-divider" />

            <!-- Offers -->
            <section v-if="offerEdits.length" class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.offers') }}</h3>
              <div v-for="(offer, i) in offerEdits" :key="i" class="list-entry">
                <div class="entry-header-row">
                  <label class="entry-label">{{ $t('editDrawer.item') }} {{ i + 1 }}</label>
                  <span v-if="offer.current !== offer.original" class="changed-badge">
                    {{ $t('editDrawer.modified') }}
                  </span>
                </div>
                <textarea v-model="offer.current" rows="2" class="edit-textarea" />
              </div>
            </section>

            <div v-if="offerEdits.length" class="section-divider" />

            <!-- Looking for -->
            <section v-if="lookingForEdits.length" class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.lookingFor') }}</h3>
              <div v-for="(item, i) in lookingForEdits" :key="i" class="list-entry">
                <div class="entry-header-row">
                  <label class="entry-label">{{ $t('editDrawer.item') }} {{ i + 1 }}</label>
                  <span v-if="item.current !== item.original" class="changed-badge">
                    {{ $t('editDrawer.modified') }}
                  </span>
                </div>
                <textarea v-model="item.current" rows="2" class="edit-textarea" />
              </div>
            </section>

            <div v-if="lookingForEdits.length" class="section-divider" />

            <!-- Website URL -->
            <section class="edit-section">
              <div class="section-header-row">
                <h3 class="section-title">{{ $t('editDrawer.website') }}</h3>
                <span v-if="isChanged('url')" class="changed-badge">{{ $t('editDrawer.modified') }}</span>
              </div>
              <input v-model="edits.url" type="text" class="edit-input" placeholder="https://" />
            </section>

            <div class="section-divider" />

            <!-- Comments + speech-to-text -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.comments') }}</h3>
              <p class="field-hint">{{ $t('editDrawer.commentsHint') }}</p>
              <div class="textarea-mic-wrap">
                <textarea
                  v-model="comments"
                  rows="4"
                  class="edit-textarea"
                  :placeholder="$t('editDrawer.commentsPlaceholder')"
                />
                <button
                  v-if="speechSupported"
                  type="button"
                  class="mic-btn"
                  :class="{ listening }"
                  :title="listening ? $t('editDrawer.stopListening') : $t('editDrawer.startListening')"
                  @click="toggleSpeech"
                >
                  <span class="mic-icon">{{ listening ? '⏹' : '🎤' }}</span>
                  <span class="mic-label">{{ listening ? $t('editDrawer.listening') : $t('editDrawer.speak') }}</span>
                </button>
              </div>
              <p v-if="listening" class="listening-hint">{{ $t('editDrawer.listeningHint') }}</p>
            </section>

            <p v-if="showValidation && !hasChanges" class="validation-error">
              {{ $t('editDrawer.validationChanges') }}
            </p>
            <p v-if="showValidation && !contact.name.trim()" class="validation-error">
              {{ $t('editDrawer.validationName') }}
            </p>
          </div>

          <!-- Footer -->
          <div class="drawer-footer">
            <Transition name="fade">
              <div v-if="submitted" class="success-message">
                ✓ {{ $t('editDrawer.success') }}
              </div>
              <div v-else-if="submitError" class="error-message">{{ submitError }}</div>
              <button
                v-else
                type="button"
                class="submit-btn"
                :disabled="submitting"
                @click="handleSubmit"
              >
                {{ submitting ? $t('editDrawer.submitting') : $t('editDrawer.submit') }}
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
  localizedDescription: string
  localizedTimeline: { date: string; icon: string; text: string }[]
  localizedOffers: { title: string; icon: string }[]
  localizedLookingFor: { title: string; icon: string }[]
  pageUrl: string
}>()

const emit = defineEmits<{ close: [] }>()
const { t, locale } = useI18n()

// ── Contact ────────────────────────────────────────────────────────────────
const contact = ref({ name: '', email: '', phone: '' })

// ── Editable state ─────────────────────────────────────────────────────────
const edits = ref({ description: '', url: '' })
const originals = ref({ description: '', url: '' })
const timelineEdits = ref<{ date: string; original: string; current: string }[]>([])
const offerEdits = ref<{ original: string; current: string }[]>([])
const lookingForEdits = ref<{ original: string; current: string }[]>([])
const comments = ref('')

const initEdits = () => {
  const proj = props.project as any
  const desc = props.localizedDescription || ''
  const url = proj?.url || ''
  originals.value = { description: desc, url }
  edits.value = { description: desc, url }

  timelineEdits.value = (props.localizedTimeline || []).map((e) => ({
    date: e.date,
    original: e.text,
    current: e.text,
  }))

  offerEdits.value = (props.localizedOffers || []).map((o) => ({
    original: o.title,
    current: o.title,
  }))

  lookingForEdits.value = (props.localizedLookingFor || []).map((l) => ({
    original: l.title,
    current: l.title,
  }))

  comments.value = ''
  contact.value = { name: '', email: '', phone: '' }
  submitted.value = false
  submitError.value = ''
  showValidation.value = false
}

watch(() => props.isOpen, (open) => { if (open) initEdits() })

// ── Change detection ───────────────────────────────────────────────────────
const isChanged = (field: 'description' | 'url') =>
  edits.value[field] !== originals.value[field]

const hasChanges = computed(
  () =>
    isChanged('description') ||
    isChanged('url') ||
    timelineEdits.value.some((e) => e.current !== e.original) ||
    offerEdits.value.some((o) => o.current !== o.original) ||
    lookingForEdits.value.some((l) => l.current !== l.original) ||
    comments.value.trim().length > 0,
)

const isContactValid = computed(
  () => contact.value.email.trim() || contact.value.phone.trim(),
)

const isValid = computed(
  () => contact.value.name.trim() && isContactValid.value && hasChanges.value,
)

// ── Submit ─────────────────────────────────────────────────────────────────
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
const showValidation = ref(false)

const buildEmailBody = (): string => {
  const proj = props.project as any
  const lines: string[] = []

  lines.push(`Project: ${props.localizedName} (#${proj?.pubId ?? ''})`)
  lines.push(`Page: ${props.pageUrl}`)
  lines.push(`Language edited: ${locale.value}`)
  lines.push('')
  lines.push(`From: ${contact.value.name}`)
  if (contact.value.email) lines.push(`Email: ${contact.value.email}`)
  if (contact.value.phone) lines.push(`Phone: ${contact.value.phone}`)
  lines.push('')

  const changed: string[] = []

  if (isChanged('description')) {
    changed.push(
      `DESCRIPTION\nBefore:\n${originals.value.description}\n\nAfter:\n${edits.value.description}`,
    )
  }

  if (isChanged('url')) {
    changed.push(`WEBSITE\nBefore: ${originals.value.url}\nAfter: ${edits.value.url}`)
  }

  for (const entry of timelineEdits.value) {
    if (entry.current !== entry.original) {
      changed.push(
        `TIMELINE — ${entry.date}\nBefore:\n${entry.original}\n\nAfter:\n${entry.current}`,
      )
    }
  }

  for (let i = 0; i < offerEdits.value.length; i++) {
    const o = offerEdits.value[i]
    if (o.current !== o.original) {
      changed.push(`OFFER ${i + 1}\nBefore: ${o.original}\nAfter: ${o.current}`)
    }
  }

  for (let i = 0; i < lookingForEdits.value.length; i++) {
    const l = lookingForEdits.value[i]
    if (l.current !== l.original) {
      changed.push(`LOOKING FOR ${i + 1}\nBefore: ${l.original}\nAfter: ${l.current}`)
    }
  }

  if (changed.length) {
    lines.push('--- CHANGES ---', '', changed.join('\n\n---\n\n'), '')
  }

  if (comments.value.trim()) {
    lines.push('--- ADDITIONAL COMMENTS ---', comments.value.trim())
  }

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
        subject: `Edit suggestion — ${props.localizedName} (#${proj?.pubId ?? ''})`,
        from_name: contact.value.name,
        email: contact.value.email || 'noreply@thesocioscope.org',
        replyto: contact.value.email || '',
        message: buildEmailBody(),
      }),
    })
    const data = await res.json()
    if (data.success) {
      submitted.value = true
    } else {
      submitError.value = t('editDrawer.error')
    }
  } catch {
    submitError.value = t('editDrawer.error')
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  emit('close')
}

// ── Speech-to-text ─────────────────────────────────────────────────────────
const speechSupported = computed(
  () =>
    import.meta.client &&
    ('SpeechRecognition' in window || 'webkitSpeechRecognition' in window),
)
const listening = ref(false)
let recognition: any = null

const LANG_MAP: Record<string, string> = {
  en: 'en-US',
  fr: 'fr-FR',
  es: 'es-ES',
  de: 'de-DE',
}

const toggleSpeech = () => {
  if (listening.value) {
    recognition?.stop()
    listening.value = false
    return
  }

  const SR =
    (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
  recognition = new SR()
  recognition.lang = LANG_MAP[locale.value] ?? 'en-US'
  recognition.continuous = true
  recognition.interimResults = false

  recognition.onresult = (event: any) => {
    const transcript = Array.from(event.results as SpeechRecognitionResultList)
      .map((r: SpeechRecognitionResult) => r[0].transcript)
      .join(' ')
    comments.value += (comments.value ? ' ' : '') + transcript
  }
  recognition.onerror = () => {
    listening.value = false
  }
  recognition.onend = () => {
    listening.value = false
  }

  recognition.start()
  listening.value = true
}
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

// ── Overlay & panel ────────────────────────────────────────────────────────
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

// ── Header ─────────────────────────────────────────────────────────────────
.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 1.5rem 1.5rem 1.25rem;
  border-bottom: 2px solid $border-cream;
  background: $forest-green;
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

// ── Scrollable body ────────────────────────────────────────────────────────
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

// ── Sections ───────────────────────────────────────────────────────────────
.edit-section {
  margin-bottom: 1.25rem;
}

.section-divider {
  height: 1px;
  background: $border-cream;
  margin: 1.25rem 0;
}

.section-header-row,
.entry-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: $brown-dark;
  margin: 0 0 0.75rem;
}

.section-header-row .section-title,
.entry-header-row + .section-title {
  margin-bottom: 0;
}

.changed-badge {
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  background: $green-bright;
  color: white;
  padding: 0.15rem 0.5rem;
  border-radius: $border-radius-pill;
}

// ── Form controls ──────────────────────────────────────────────────────────
.form-group {
  margin-bottom: 0.85rem;

  label {
    display: block;
    font-size: 0.8rem;
    font-weight: 600;
    color: $brown-dark;
    margin-bottom: 0.3rem;
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

.edit-input,
.edit-textarea,
.form-group input {
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
    border-color: $green-bright;
  }
}

.edit-textarea {
  resize: vertical;
  min-height: 60px;
}

.field-hint {
  font-size: 0.78rem;
  color: $brown-medium;
  margin: 0.25rem 0 0;
  opacity: 0.85;
}

// ── List entries (timeline / offers / looking-for) ─────────────────────────
.list-entry {
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px dashed $border-cream;

  &:last-child {
    border-bottom: none;
    margin-bottom: 0;
    padding-bottom: 0;
  }
}

.entry-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: $brown-medium;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

// ── Speech / mic ───────────────────────────────────────────────────────────
.textarea-mic-wrap {
  position: relative;
}

.mic-btn {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 0.5rem;
  background: white;
  border: 1.5px solid $border-cream;
  border-radius: $border-radius-pill;
  padding: 0.4rem 0.85rem;
  font-size: 0.82rem;
  font-family: $font-family-base;
  color: $brown-dark;
  cursor: pointer;
  transition: all $transition-fast;

  &:hover {
    border-color: $green-bright;
    color: $green-bright;
  }

  &.listening {
    background: #fff0f0;
    border-color: #e53935;
    color: #e53935;
    animation: pulse 1.2s ease-in-out infinite;
  }
}

.mic-icon {
  font-size: 1rem;
}

.listening-hint {
  font-size: 0.78rem;
  color: #e53935;
  margin: 0.3rem 0 0;
  font-style: italic;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

// ── Validation ─────────────────────────────────────────────────────────────
.validation-error {
  font-size: 0.82rem;
  color: #e53935;
  margin: 0.4rem 0 0;
}

// ── Footer ─────────────────────────────────────────────────────────────────
.drawer-footer {
  padding: 1rem 1.5rem;
  border-top: 2px solid $border-cream;
  background: $cream;
  flex-shrink: 0;
}

.submit-btn {
  width: 100%;
  background: $forest-green;
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
  color: $green-bright;
  font-size: 0.95rem;
  padding: 0.5rem 0;
}

.error-message {
  text-align: center;
  color: #e53935;
  font-size: 0.88rem;
  padding: 0.5rem 0;
}

// ── Drawer slide-in transition ─────────────────────────────────────────────
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

// ── Fade transition (footer messages) ─────────────────────────────────────
.fade-enter-active,
.fade-leave-active {
  transition: opacity $transition-fast;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
