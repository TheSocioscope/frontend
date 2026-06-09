<template>
  <div class="research-form-wrapper">
    <!-- Research Selection Section -->
    <div class="research-sections">
      <!-- Strategic Tools -->
      <section class="research-section">
        <h2 class="section-title">
          <span class="emoji">🔍</span>
          Strategic Tools
        </h2>
        <p class="section-desc">Structured assessments and strategic documents built from your data</p>
        <div class="checkboxes-grid">
          <label v-for="item in strategicTools" :key="item.id" class="checkbox-label">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <span class="checkbox-text">{{ item.label }}</span>
          </label>
        </div>
      </section>

      <!-- Benchmarking & Research -->
      <section class="research-section">
        <h2 class="section-title">
          <span class="emoji">📊</span>
          Benchmarking & Research
        </h2>
        <p class="section-desc">Data-driven insights into your positioning and opportunities</p>
        <div class="checkboxes-grid">
          <label v-for="item in benchmarkingTools" :key="item.id" class="checkbox-label">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <span class="checkbox-text">{{ item.label }}</span>
          </label>
        </div>
      </section>

      <!-- Visibility & Recognition -->
      <section class="research-section">
        <h2 class="section-title">
          <span class="emoji">📣</span>
          Visibility & Recognition
        </h2>
        <p class="section-desc">Amplify your story and build external credibility</p>
        <div class="checkboxes-grid">
          <label v-for="item in visibilityTools" :key="item.id" class="checkbox-label">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <span class="checkbox-text">{{ item.label }}</span>
          </label>
        </div>
      </section>

      <!-- Collective & Learning -->
      <section class="research-section">
        <h2 class="section-title">
          <span class="emoji">🤝</span>
          Collective & Learning
        </h2>
        <p class="section-desc">Connect with peers and share knowledge</p>
        <div class="checkboxes-grid">
          <label v-for="item in collectiveTools" :key="item.id" class="checkbox-label">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <span class="checkbox-text">{{ item.label }}</span>
          </label>
        </div>
      </section>
    </div>

    <!-- Additional Info for Selected Items -->
    <div v-if="selectedItems.length > 0" class="selected-items-section">
      <h3 class="subsection-title">Tell us more about your interests</h3>
      <div class="additional-info-cards">
        <div v-for="itemId in selectedItems" :key="itemId" class="info-card">
          <h4>{{ getItemLabel(itemId) }}</h4>
          <textarea
            v-model="additionalInfo[itemId]"
            placeholder="How would you use this? What specific questions do you want answered?"
            rows="3"
            class="info-textarea"
          />
        </div>
      </div>
    </div>

    <!-- Contact Info Section -->
    <div class="contact-section">
      <h3 class="subsection-title">Your Contact Information</h3>

      <div class="form-group">
        <label>Initiative Name *</label>
        <input v-model="form.initiativeName" type="text" placeholder="Your organization name" required />
      </div>

      <div class="form-row">
        <div class="form-group">
          <label>Your Name *</label>
          <input v-model="form.name" type="text" placeholder="Your full name" required />
        </div>
        <div class="form-group">
          <label>Email *</label>
          <input v-model="form.email" type="email" placeholder="your@email.com" required />
        </div>
      </div>

      <div class="form-group">
        <label>Phone</label>
        <input v-model="form.phone" type="tel" placeholder="+1 234 567 8900" />
      </div>

      <div class="form-group">
        <label>Additional Notes</label>
        <textarea
          v-model="form.notes"
          placeholder="Any other information you'd like to share..."
          rows="3"
        />
      </div>

      <!-- Error/Success Messages -->
      <p v-if="validationError" class="error-message">{{ validationError }}</p>

      <Transition name="fade">
        <div v-if="submitted" class="success-message">
          ✓ Thank you! We've received your request and will be in touch soon.
        </div>
        <button
          v-else
          type="button"
          class="submit-btn"
          :disabled="submitting || selectedItems.length === 0"
          @click="handleSubmit"
        >
          {{ submitting ? 'Sending...' : 'Submit Research Request' }}
        </button>
      </Transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import { web3formsKey } from '~~/static.config'

// Research items
const strategicTools = [
  { id: 'swot', label: 'SWOT analysis — Strengths, Weaknesses, Opportunities, Threats' },
  { id: 'transaction', label: 'Transaction grid — Map exchanges and value flows with partners' },
  { id: 'stakeholder', label: 'Stakeholder map — Visualise your relational ecosystem' },
  { id: 'barriers', label: 'Analysis of your specific barriers — What\'s holding you back' },
  { id: 'whatWorked', label: 'Personalised "what worked elsewhere" memo — 3–4 proven strategies' },
]

const benchmarkingTools = [
  { id: 'positioning', label: 'Positioning benchmark — Where you stand among 600+ initiatives' },
  { id: 'timeline', label: 'Transition timeline — Your initiative\'s evolution visualised' },
  { id: 'sectorReport', label: 'Access to a thematic sector report — Tailored to your area' },
  { id: 'funding', label: 'Funding opportunities analysis — Cross-referenced with your profile' },
]

const visibilityTools = [
  { id: 'narrative', label: 'Narrative portrait / valorisation sheet — Polished case study' },
  { id: 'mention', label: 'Mention in publications — Credited as a contributor' },
  { id: 'certificate', label: '"Food Socioscope Contributor" certificate or label' },
]

const collectiveTools = [
  { id: 'peerLearning', label: 'Peer learning sessions — Small group workshops with 5–6 initiatives' },
  { id: 'webinar', label: 'Webinar hosting — We host your training session' },
]

// Form state
const selectedItems = ref<string[]>([])
const additionalInfo = ref<Record<string, string>>({})
const form = ref({
  initiativeName: '',
  name: '',
  email: '',
  phone: '',
  notes: '',
})

const submitting = ref(false)
const submitted = ref(false)
const validationError = ref('')

const getItemLabel = (id: string): string => {
  const allTools = [...strategicTools, ...benchmarkingTools, ...visibilityTools, ...collectiveTools]
  return allTools.find((t) => t.id === id)?.label || id
}

const handleSubmit = async () => {
  validationError.value = ''

  // Validate
  if (!form.value.initiativeName.trim()) {
    validationError.value = 'Initiative name is required'
    return
  }
  if (!form.value.name.trim()) {
    validationError.value = 'Name is required'
    return
  }
  if (!form.value.email.trim()) {
    validationError.value = 'Email is required'
    return
  }
  if (selectedItems.value.length === 0) {
    validationError.value = 'Please select at least one research item'
    return
  }

  submitting.value = true

  try {
    // Build email body
    const selectedLabels = selectedItems.value.map((id) => {
      const label = getItemLabel(id)
      const info = additionalInfo.value[id]
      return `• ${label}${info ? `\n  Details: ${info}` : ''}`
    })

    const emailBody = `
New Research Request

INITIATIVE: ${form.value.initiativeName}

CONTACT INFO:
Name: ${form.value.name}
Email: ${form.value.email}
${form.value.phone ? `Phone: ${form.value.phone}\n` : ''}

RESEARCH INTERESTS:
${selectedLabels.join('\n')}

${form.value.notes ? `\nADDITIONAL NOTES:\n${form.value.notes}` : ''}
`

    const formData = new FormData()
    formData.append('access_key', web3formsKey)
    formData.append('to', 'thesocioscope.org@gmail.com')
    formData.append('subject', `Food Socioscope Research Request — ${form.value.initiativeName}`)
    formData.append('from_name', form.value.name)
    formData.append('email', form.value.email)
    formData.append('message', emailBody)

    const res = await fetch('https://api.web3forms.com/submit', { method: 'POST', body: formData })
    const data = await res.json()

    if (data.success) {
      submitted.value = true
      // Reset form after 3 seconds
      setTimeout(() => {
        selectedItems.value = []
        additionalInfo.value = {}
        form.value = { initiativeName: '', name: '', email: '', phone: '', notes: '' }
        submitted.value = false
      }, 3000)
    } else {
      validationError.value = 'Failed to send request. Please try again.'
    }
  } catch (error) {
    validationError.value = 'An error occurred. Please try again.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.research-form-wrapper {
  background: white;
  border-radius: $border-radius-lg;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);

  @media (max-width: 768px) {
    padding: 1.5rem;
  }
}

// Research Sections
.research-sections {
  display: flex;
  flex-direction: column;
  gap: 2.5rem;
  margin-bottom: 2.5rem;
}

.research-section {
  border-left: 4px solid $green-bright;
  padding-left: 1.5rem;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 1.25rem;
  font-weight: 700;
  color: $brown-dark;
  margin: 0 0 0.5rem;

  .emoji {
    font-size: 1.5rem;
  }
}

.section-desc {
  font-size: 0.9rem;
  color: $brown-medium;
  margin: 0 0 1.25rem;
  line-height: 1.5;
}

.checkboxes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 0.75rem;

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 0.75rem;
  border-radius: $border-radius-md;
  cursor: pointer;
  transition: background-color $transition-fast;
  user-select: none;

  &:hover {
    background: $cream-dark;
  }

  .checkbox-input {
    width: 20px;
    height: 20px;
    margin-top: 2px;
    cursor: pointer;
    accent-color: $green-bright;
    flex-shrink: 0;
  }

  .checkbox-text {
    font-size: 0.9rem;
    color: $brown-dark;
    line-height: 1.4;
  }
}

// Selected Items Section
.selected-items-section {
  background: $cream-dark;
  padding: 1.5rem;
  border-radius: $border-radius-md;
  margin-bottom: 2rem;
}

.subsection-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: $brown-dark;
  margin: 0 0 1.25rem;
}

.additional-info-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1rem;
}

.info-card {
  background: white;
  padding: 1rem;
  border-radius: $border-radius-md;
  border: 1px solid $border-cream;

  h4 {
    font-size: 0.9rem;
    color: $brown-dark;
    margin: 0 0 0.75rem;
    line-height: 1.4;
  }
}

.info-textarea {
  width: 100%;
  padding: 0.75rem;
  border: 1.5px solid $border-cream;
  border-radius: $border-radius-md;
  font-size: 0.85rem;
  font-family: $font-family-base;
  color: $brown-dark;
  resize: vertical;
  transition: border-color $transition-fast;
  box-sizing: border-box;

  &:focus {
    outline: none;
    border-color: $green-bright;
  }

  &::placeholder {
    color: $text-caption;
  }
}

// Contact Section
.contact-section {
  border-top: 2px solid $border-cream;
  padding-top: 2rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;

  @media (max-width: 600px) {
    grid-template-columns: 1fr;
  }
}

.form-group {
  margin-bottom: 1.25rem;

  label {
    display: block;
    font-size: 0.9rem;
    font-weight: 600;
    color: $brown-dark;
    margin-bottom: 0.4rem;
  }

  input,
  textarea {
    width: 100%;
    padding: 0.75rem;
    border: 1.5px solid $border-cream;
    border-radius: $border-radius-md;
    font-size: 0.9rem;
    font-family: $font-family-base;
    color: $brown-dark;
    background: white;
    transition: border-color $transition-fast;
    box-sizing: border-box;

    &:focus {
      outline: none;
      border-color: $green-bright;
    }

    &::placeholder {
      color: $text-caption;
    }
  }

  textarea {
    resize: vertical;
    min-height: 80px;
  }
}

// Messages
.error-message {
  color: #c0392b;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(192, 57, 43, 0.08);
  border-radius: $border-radius-md;
  border-left: 3px solid #c0392b;
}

.success-message {
  color: $green-bright;
  font-size: 0.95rem;
  text-align: center;
  padding: 1rem;
  background: rgba(76, 160, 73, 0.08);
  border-radius: $border-radius-md;
  border-left: 3px solid $green-bright;
}

.submit-btn {
  width: 100%;
  padding: 1rem;
  background: $forest-green;
  color: white;
  border: none;
  border-radius: $border-radius-md;
  font-size: 0.95rem;
  font-weight: 700;
  font-family: $font-family-base;
  cursor: pointer;
  transition: all $transition-fast;
  margin-top: 1.5rem;

  &:hover:not(:disabled) {
    background: $green-bright;
    transform: translateY(-2px);
    box-shadow: $shadow-md;
  }

  &:disabled {
    opacity: 0.55;
    cursor: not-allowed;
  }
}

// Transitions
.fade-enter-active,
.fade-leave-active {
  transition: opacity $transition-fast;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
