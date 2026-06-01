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

            <!-- 1. Contact details -->
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

            <!-- 2. Name & tagline -->
            <section class="edit-section">
              <div class="section-header-row">
                <h3 class="section-title">{{ $t('editDrawer.nameTagline', 'Name & tagline') }}</h3>
                <span v-if="isChanged('name') || isChanged('tagline')" class="changed-badge">
                  {{ $t('editDrawer.modified') }}
                </span>
              </div>
              <div class="form-group">
                <label>{{ $t('editDrawer.projectName', 'Project name') }}</label>
                <input v-model="edits.name" type="text" class="edit-input" />
              </div>
              <div class="form-group">
                <label>{{ $t('editDrawer.tagline', 'Tagline') }}</label>
                <input v-model="edits.tagline" type="text" class="edit-input" :placeholder="$t('editDrawer.taglinePlaceholder', 'Short summary sentence')" />
              </div>
            </section>

            <div class="section-divider" />

            <!-- 3. Description -->
            <section class="edit-section">
              <div class="section-header-row">
                <h3 class="section-title">{{ $t('editDrawer.description') }}</h3>
                <span v-if="isChanged('description')" class="changed-badge">{{ $t('editDrawer.modified') }}</span>
              </div>
              <textarea v-model="edits.description" rows="6" class="edit-textarea" />
            </section>

            <div class="section-divider" />

            <!-- 4. Team members -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.team', 'Team members') }}</h3>

              <!-- Existing team read-only -->
              <div v-if="existingTeam.length" class="team-ref-list">
                <span v-for="(member, i) in existingTeam" :key="i" class="team-ref-chip">
                  {{ member.firstname }} {{ member.lastname }}<template v-if="member.role"> — {{ member.role }}</template>
                </span>
              </div>

              <!-- New member entries -->
              <div
                v-for="(member, i) in newTeamMembers"
                :key="i"
                class="new-member-entry"
              >
                <div class="form-row">
                  <div class="form-group">
                    <label>{{ $t('editDrawer.teamFirstname', 'First name') }}</label>
                    <input v-model="member.firstname" type="text" class="edit-input" />
                  </div>
                  <div class="form-group">
                    <label>{{ $t('editDrawer.teamLastname', 'Last name') }}</label>
                    <input v-model="member.lastname" type="text" class="edit-input" />
                  </div>
                </div>
                <div class="form-row">
                  <div class="form-group">
                    <label>{{ $t('editDrawer.teamRole', 'Role') }}</label>
                    <input v-model="member.role" type="text" class="edit-input" />
                  </div>
                  <div class="form-group">
                    <label>{{ $t('editDrawer.teamEntity', 'Entity / organisation') }}</label>
                    <input v-model="member.entity" type="text" class="edit-input" />
                  </div>
                </div>
                <button type="button" class="entry-remove-btn" @click="removeTeamMember(i)">
                  {{ $t('editDrawer.remove', 'Remove') }}
                </button>
              </div>

              <button type="button" class="add-member-btn" @click="addTeamMember">
                <v-icon size="16">mdi-plus</v-icon>
                {{ $t('editDrawer.addTeamMember', '+ Add team member') }}
              </button>
            </section>

            <!-- 5. Offers -->
            <template v-if="offerEdits.length">
              <div class="section-divider" />
              <section class="edit-section">
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
            </template>

            <!-- 6. Looking for -->
            <template v-if="lookingForEdits.length">
              <div class="section-divider" />
              <section class="edit-section">
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
            </template>

            <!-- 7. Timeline -->
            <template v-if="timelineEdits.length">
              <div class="section-divider" />
              <section class="edit-section">
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
            </template>

            <div class="section-divider" />

            <!-- 8. Photos -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.photos', 'Photos') }}</h3>
              <label class="file-upload-area" for="photo-upload">
                <v-icon class="file-upload-icon">mdi-image-plus</v-icon>
                <span class="file-upload-text">
                  {{ $t('editDrawer.choosePhotos', 'Choose photos or drag and drop') }}
                </span>
                <span class="file-upload-hint">
                  {{ $t('editDrawer.photoHint', 'Up to 5 files · max 5 MB each · images only') }}
                </span>
              </label>
              <input
                id="photo-upload"
                type="file"
                accept="image/*"
                multiple
                class="file-input-hidden"
                @change="handleFileChange"
              />
              <p v-if="fileError" class="file-error">{{ fileError }}</p>
              <div v-if="attachedFiles.length" class="file-list">
                <div v-for="(file, i) in attachedFiles" :key="i" class="file-chip">
                  <v-icon size="14">mdi-image</v-icon>
                  <span class="file-chip-name">{{ file.name }}</span>
                  <button type="button" class="file-chip-remove" @click="removeFile(i)">&times;</button>
                </div>
              </div>
            </section>

            <div class="section-divider" />

            <!-- 9. Website URL -->
            <section class="edit-section">
              <div class="section-header-row">
                <h3 class="section-title">{{ $t('editDrawer.website') }}</h3>
                <span v-if="isChanged('url')" class="changed-badge">{{ $t('editDrawer.modified') }}</span>
              </div>
              <input v-model="edits.url" type="text" class="edit-input" placeholder="https://" />
            </section>

            <div class="section-divider" />

            <!-- 10. Comments + speech-to-text -->
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
  localizedTagline?: string
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
const edits = ref({ description: '', url: '', name: '', tagline: '' })
const originals = ref({ description: '', url: '', name: '', tagline: '' })
const timelineEdits = ref<{ date: string; original: string; current: string }[]>([])
const offerEdits = ref<{ original: string; current: string }[]>([])
const lookingForEdits = ref<{ original: string; current: string }[]>([])
const comments = ref('')

// ── Team & file state ──────────────────────────────────────────────────────
const newTeamMembers = ref<{ firstname: string; lastname: string; role: string; entity: string }[]>([])
const attachedFiles = ref<File[]>([])
const fileError = ref('')
const MAX_FILES = 5
const MAX_SIZE_MB = 5

// ── Existing team (read-only display) ─────────────────────────────────────
const existingTeam = computed(() => {
  const proj = props.project as any
  if (!proj?.team || !Array.isArray(proj.team)) return []
  return proj.team.map((m: any) => ({
    firstname: m.firstname || m.first_name || '',
    lastname: m.lastname || m.last_name || '',
    role: m.role || '',
  }))
})

const initEdits = () => {
  const proj = props.project as any
  const desc = props.localizedDescription || ''
  const url = proj?.url || ''
  const name = props.localizedName || ''
  const tagline = props.localizedTagline || ''
  originals.value = { description: desc, url, name, tagline }
  edits.value = { ...originals.value }

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
  newTeamMembers.value = []
  attachedFiles.value = []
  fileError.value = ''
}

watch(() => props.isOpen, (open) => { if (open) initEdits() })

// ── Change detection ───────────────────────────────────────────────────────
const isChanged = (field: 'description' | 'url' | 'name' | 'tagline') =>
  edits.value[field] !== originals.value[field]

const hasChanges = computed(
  () =>
    isChanged('description') ||
    isChanged('url') ||
    isChanged('name') ||
    isChanged('tagline') ||
    timelineEdits.value.some((e) => e.current !== e.original) ||
    offerEdits.value.some((o) => o.current !== o.original) ||
    lookingForEdits.value.some((l) => l.current !== l.original) ||
    comments.value.trim().length > 0 ||
    newTeamMembers.value.some((m) => m.firstname.trim() || m.lastname.trim()) ||
    attachedFiles.value.length > 0,
)

const isContactValid = computed(
  () => contact.value.email.trim() || contact.value.phone.trim(),
)

const isValid = computed(
  () => contact.value.name.trim() && isContactValid.value && hasChanges.value,
)

// ── Team member helpers ────────────────────────────────────────────────────
const addTeamMember = () => {
  newTeamMembers.value.push({ firstname: '', lastname: '', role: '', entity: '' })
}

const removeTeamMember = (index: number) => {
  newTeamMembers.value.splice(index, 1)
}

// ── File upload helpers ────────────────────────────────────────────────────
const handleFileChange = (event: Event) => {
  fileError.value = ''
  const input = event.target as HTMLInputElement
  if (!input.files) return

  const incoming = Array.from(input.files)
  const oversized = incoming.filter((f) => f.size > MAX_SIZE_MB * 1024 * 1024)
  if (oversized.length) {
    fileError.value = `${oversized.map((f) => f.name).join(', ')} exceed${oversized.length === 1 ? 's' : ''} the ${MAX_SIZE_MB} MB limit.`
    input.value = ''
    return
  }

  const combined = [...attachedFiles.value, ...incoming]
  if (combined.length > MAX_FILES) {
    fileError.value = `You can attach at most ${MAX_FILES} photos. ${combined.length - MAX_FILES} file(s) were not added.`
    attachedFiles.value = combined.slice(0, MAX_FILES)
  } else {
    attachedFiles.value = combined
  }
  input.value = ''
}

const removeFile = (index: number) => {
  attachedFiles.value.splice(index, 1)
  fileError.value = ''
}

// ── Submit ─────────────────────────────────────────────────────────────────
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
const showValidation = ref(false)

const wordDiff = (original: string, current: string): string => {
  const a = original.split(/\s+/).filter(Boolean)
  const b = current.split(/\s+/).filter(Boolean)
  const m = a.length
  const n = b.length
  const dp: number[][] = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0))
  for (let i = 1; i <= m; i++)
    for (let j = 1; j <= n; j++)
      dp[i][j] = a[i - 1] === b[j - 1] ? dp[i - 1][j - 1] + 1 : Math.max(dp[i - 1][j], dp[i][j - 1])
  const parts: string[] = []
  let i = m
  let j = n
  while (i > 0 || j > 0) {
    if (i > 0 && j > 0 && a[i - 1] === b[j - 1]) {
      parts.unshift(a[i - 1])
      i--
      j--
    } else if (j > 0 && (i === 0 || dp[i][j - 1] >= dp[i - 1][j])) {
      parts.unshift(`{+${b[j - 1]}+}`)
      j--
    } else {
      parts.unshift(`[-${a[i - 1]}-]`)
      i--
    }
  }
  return parts.join(' ')
}

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

  if (isChanged('name')) {
    changed.push(
      `NAME\nBefore: ${originals.value.name}\nAfter: ${edits.value.name}`,
    )
  }

  if (isChanged('tagline')) {
    changed.push(
      `TAGLINE\nBefore: ${originals.value.tagline}\nAfter: ${edits.value.tagline}`,
    )
  }

  if (isChanged('description')) {
    changed.push(
      `DESCRIPTION\nBefore:\n${originals.value.description}\n\nAfter:\n${edits.value.description}\n\nDiff:\n${wordDiff(originals.value.description, edits.value.description)}`,
    )
  }

  if (isChanged('url')) {
    changed.push(
      `WEBSITE\nBefore: ${originals.value.url}\nAfter: ${edits.value.url}\nDiff: ${wordDiff(originals.value.url, edits.value.url)}`,
    )
  }

  for (const entry of timelineEdits.value) {
    if (entry.current !== entry.original) {
      changed.push(
        `TIMELINE — ${entry.date}\nBefore:\n${entry.original}\n\nAfter:\n${entry.current}\n\nDiff:\n${wordDiff(entry.original, entry.current)}`,
      )
    }
  }

  for (let idx = 0; idx < offerEdits.value.length; idx++) {
    const o = offerEdits.value[idx]
    if (o.current !== o.original) {
      changed.push(
        `OFFER ${idx + 1}\nBefore: ${o.original}\nAfter: ${o.current}\nDiff: ${wordDiff(o.original, o.current)}`,
      )
    }
  }

  for (let idx = 0; idx < lookingForEdits.value.length; idx++) {
    const l = lookingForEdits.value[idx]
    if (l.current !== l.original) {
      changed.push(
        `LOOKING FOR ${idx + 1}\nBefore: ${l.original}\nAfter: ${l.current}\nDiff: ${wordDiff(l.original, l.current)}`,
      )
    }
  }

  if (changed.length) {
    lines.push('--- CHANGES ---', '', changed.join('\n\n---\n\n'), '')
  }

  const newMembersToReport = newTeamMembers.value.filter(
    (m) => m.firstname.trim() || m.lastname.trim(),
  )
  if (newMembersToReport.length) {
    lines.push('--- NEW TEAM MEMBERS SUGGESTED ---')
    for (const m of newMembersToReport) {
      const fullName = [m.firstname.trim(), m.lastname.trim()].filter(Boolean).join(' ')
      const rolePart = m.role.trim() ? ` (${m.role.trim()})` : ''
      const entityPart = m.entity.trim() ? ` — ${m.entity.trim()}` : ''
      lines.push(`  - ${fullName}${rolePart}${entityPart}`)
    }
    lines.push('')
  }

  if (attachedFiles.value.length) {
    lines.push(`PHOTOS ATTACHED: ${attachedFiles.value.length} file(s) — see email attachments`)
    lines.push('')
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
    const formData = new FormData()
    formData.append('access_key', web3formsKey)
    formData.append('to', 'thesocioscope.org@gmail.com')
    formData.append('subject', `Edit suggestion — ${props.localizedName} (#${proj?.pubId ?? ''})`)
    formData.append('from_name', contact.value.name)
    formData.append('email', contact.value.email || 'noreply@thesocioscope.org')
    if (contact.value.email) formData.append('replyto', contact.value.email)
    formData.append('message', buildEmailBody())
    attachedFiles.value.forEach((file) => formData.append('attachment[]', file, file.name))

    const res = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: formData })
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

/* ── Team section ────────────────────────────────────────────── */
.team-ref-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 0.75rem;
}

.team-ref-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.78rem;
  font-weight: 600;
  background: rgba(76, 160, 73, 0.1);
  color: #27421d;
  border: 0.5px solid rgba(76, 160, 73, 0.3);
  border-radius: 999px;
  padding: 3px 10px;
}

.new-member-entry {
  border: 1px dashed $border-cream;
  border-radius: $border-radius-md;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: $cream-dark;
}

.entry-remove-btn {
  background: none;
  border: none;
  font-size: 0.78rem;
  color: #c0392b;
  cursor: pointer;
  padding: 0.2rem 0;
  margin-top: 0.25rem;
  text-decoration: underline;
  font-family: $font-family-base;

  &:hover {
    color: darken(#c0392b, 10%);
  }
}

.add-member-btn {
  display: flex;
  align-items: center;
  gap: 5px;
  background: none;
  border: 1.5px dashed $border-cream;
  border-radius: $border-radius-md;
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
  font-family: $font-family-base;
  color: $brown-medium;
  cursor: pointer;
  width: 100%;
  justify-content: center;
  transition: border-color $transition-fast, color $transition-fast;

  &:hover {
    border-color: $green-bright;
    color: $green-bright;
  }
}

/* ── Photo upload section ────────────────────────────────────── */
.file-upload-area {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  border: 1.5px dashed $border-cream;
  border-radius: $border-radius-md;
  padding: 1.25rem;
  text-align: center;
  cursor: pointer;
  transition: border-color $transition-fast, background $transition-fast;
  background: $cream-dark;

  &:hover {
    border-color: $green-bright;
    background: rgba(76, 160, 73, 0.04);
  }
}

.file-upload-icon {
  font-size: 1.5rem;
  color: $green-bright;
}

.file-upload-text {
  font-size: 0.85rem;
  color: $brown-medium;
  font-weight: 500;
}

.file-upload-hint {
  font-size: 0.75rem;
  color: $text-caption;
}

.file-input-hidden {
  display: none;
}

.file-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 0.5rem;
}

.file-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  background: white;
  border: 0.5px solid $border-cream;
  border-radius: $border-radius-md;
  padding: 5px 10px;
  font-size: 0.82rem;
  color: $brown-dark;
}

.file-chip-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-chip-remove {
  background: none;
  border: none;
  color: $brown-medium;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0;
  flex-shrink: 0;

  &:hover {
    color: #c0392b;
  }
}

.file-error {
  font-size: 0.78rem;
  color: #c0392b;
  margin-top: 0.3rem;
}
</style>
