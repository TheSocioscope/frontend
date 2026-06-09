<template>
  <div class="research-form-wrapper">
    <!-- Research Selection Section -->
    <div class="research-sections">
      <!-- Strategic Tools -->
      <section class="research-section">
        <h2 class="section-title">Strategic Tools</h2>
        <p class="section-desc">Structured assessments and strategic documents built from your data</p>
        <div class="cards-grid">
          <label v-for="item in strategicTools" :key="item.id" class="research-card">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <div class="card-visual" :style="{ backgroundColor: item.color }">
              <v-icon size="40" color="white">{{ item.icon }}</v-icon>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ item.shortLabel }}</h3>
              <p class="card-desc">{{ item.label }}</p>
            </div>
            <div class="checkmark">
              <v-icon v-if="selectedItems.includes(item.id)" size="20" color="white">
                mdi-check
              </v-icon>
            </div>
          </label>
        </div>
      </section>

      <!-- Benchmarking & Research -->
      <section class="research-section">
        <h2 class="section-title">Benchmarking & Research</h2>
        <p class="section-desc">Data-driven insights into your positioning and opportunities</p>
        <div class="cards-grid">
          <label v-for="item in benchmarkingTools" :key="item.id" class="research-card">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <div class="card-visual" :style="{ backgroundColor: item.color }">
              <v-icon size="40" color="white">{{ item.icon }}</v-icon>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ item.shortLabel }}</h3>
              <p class="card-desc">{{ item.label }}</p>
            </div>
            <div class="checkmark">
              <v-icon v-if="selectedItems.includes(item.id)" size="20" color="white">
                mdi-check
              </v-icon>
            </div>
          </label>
        </div>
      </section>

      <!-- Visibility & Recognition -->
      <section class="research-section">
        <h2 class="section-title">Visibility & Recognition</h2>
        <p class="section-desc">Amplify your story and build external credibility</p>
        <div class="cards-grid">
          <label v-for="item in visibilityTools" :key="item.id" class="research-card">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <div class="card-visual" :style="{ backgroundColor: item.color }">
              <v-icon size="40" color="white">{{ item.icon }}</v-icon>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ item.shortLabel }}</h3>
              <p class="card-desc">{{ item.label }}</p>
            </div>
            <div class="checkmark">
              <v-icon v-if="selectedItems.includes(item.id)" size="20" color="white">
                mdi-check
              </v-icon>
            </div>
          </label>
        </div>
      </section>

      <!-- Collective & Learning -->
      <section class="research-section">
        <h2 class="section-title">Collective & Learning</h2>
        <p class="section-desc">Connect with peers and share knowledge</p>
        <div class="cards-grid">
          <label v-for="item in collectiveTools" :key="item.id" class="research-card">
            <input
              v-model="selectedItems"
              type="checkbox"
              :value="item.id"
              class="checkbox-input"
            />
            <div class="card-visual" :style="{ backgroundColor: item.color }">
              <v-icon size="40" color="white">{{ item.icon }}</v-icon>
            </div>
            <div class="card-content">
              <h3 class="card-title">{{ item.shortLabel }}</h3>
              <p class="card-desc">{{ item.label }}</p>
            </div>
            <div class="checkmark">
              <v-icon v-if="selectedItems.includes(item.id)" size="20" color="white">
                mdi-check
              </v-icon>
            </div>
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

// Research items with visual styling
const strategicTools = [
  {
    id: 'swot',
    label: 'SWOT analysis — Strengths, Weaknesses, Opportunities, Threats',
    shortLabel: 'SWOT Analysis',
    icon: 'mdi-chart-box-outline',
    color: '#E8C47A',
  },
  {
    id: 'transaction',
    label: 'Transaction grid — Map exchanges and value flows with partners',
    shortLabel: 'Transaction Grid',
    icon: 'mdi-sitemap',
    color: '#C4A890',
  },
  {
    id: 'stakeholder',
    label: 'Stakeholder map — Visualise your relational ecosystem',
    shortLabel: 'Stakeholder Map',
    icon: 'mdi-network',
    color: '#85C49A',
  },
  {
    id: 'barriers',
    label: 'Analysis of your specific barriers — What\'s holding you back',
    shortLabel: 'Barriers Analysis',
    icon: 'mdi-alert-circle-outline',
    color: '#D4A574',
  },
  {
    id: 'whatWorked',
    label: 'Personalised "what worked elsewhere" memo — 3–4 proven strategies',
    shortLabel: 'What Worked Elsewhere',
    icon: 'mdi-lightbulb-on-outline',
    color: '#A8D5BA',
  },
]

const benchmarkingTools = [
  {
    id: 'positioning',
    label: 'Positioning benchmark — Where you stand among 600+ initiatives',
    shortLabel: 'Positioning Benchmark',
    icon: 'mdi-chart-line',
    color: '#7CB8D4',
  },
  {
    id: 'timeline',
    label: 'Transition timeline — Your initiative\'s evolution visualised',
    shortLabel: 'Transition Timeline',
    icon: 'mdi-timeline-outline',
    color: '#6BA3C8',
  },
  {
    id: 'sectorReport',
    label: 'Access to a thematic sector report — Tailored to your area',
    shortLabel: 'Sector Report',
    icon: 'mdi-file-document-outline',
    color: '#8EC4D4',
  },
  {
    id: 'funding',
    label: 'Funding opportunities analysis — Cross-referenced with your profile',
    shortLabel: 'Funding Opportunities',
    icon: 'mdi-cash-multiple',
    color: '#5BA0D0',
  },
]

const visibilityTools = [
  {
    id: 'narrative',
    label: 'Narrative portrait / valorisation sheet — Polished case study',
    shortLabel: 'Narrative Portrait',
    icon: 'mdi-pencil-outline',
    color: '#E8A8A3',
  },
  {
    id: 'mention',
    label: 'Mention in publications — Credited as a contributor',
    shortLabel: 'Publication Mention',
    icon: 'mdi-newspaper-variant-outline',
    color: '#D98A88',
  },
  {
    id: 'certificate',
    label: '"Food Socioscope Contributor" certificate or label',
    shortLabel: 'Contributor Certificate',
    icon: 'mdi-medal-outline',
    color: '#E09898',
  },
]

const collectiveTools = [
  {
    id: 'peerLearning',
    label: 'Peer learning sessions — Small group workshops with 5–6 initiatives',
    shortLabel: 'Peer Learning',
    icon: 'mdi-account-group-outline',
    color: '#B8A8D4',
  },
  {
    id: 'webinar',
    label: 'Webinar hosting — We host your training session',
    shortLabel: 'Webinar Hosting',
    icon: 'mdi-video-outline',
    color: '#A896C8',
  },
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
  font-size: 1.25rem;
  font-weight: 700;
  color: $brown-dark;
  margin: 0 0 0.5rem;
}

.section-desc {
  font-size: 0.9rem;
  color: $brown-medium;
  margin: 0 0 1.25rem;
  line-height: 1.5;
}

.cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.25rem;

  @media (max-width: 768px) {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
    gap: 1rem;
  }

  @media (max-width: 500px) {
    grid-template-columns: repeat(2, 1fr);
  }
}

.research-card {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem;
  border: 2px solid $border-cream;
  border-radius: $border-radius-lg;
  background: white;
  cursor: pointer;
  transition: all $transition-fast;
  text-align: center;

  &:hover {
    border-color: $green-bright;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
    transform: translateY(-4px);
  }

  .checkbox-input {
    position: absolute;
    top: 10px;
    right: 10px;
    width: 18px;
    height: 18px;
    cursor: pointer;
    accent-color: $green-bright;
  }

  .card-visual {
    width: 80px;
    height: 80px;
    border-radius: $border-radius-md;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: transform $transition-fast;
  }

  &:hover .card-visual {
    transform: scale(1.1);
  }

  .card-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }

  .card-title {
    font-size: 0.95rem;
    font-weight: 700;
    color: $brown-dark;
    margin: 0;
    line-height: 1.3;
  }

  .card-desc {
    font-size: 0.75rem;
    color: $brown-medium;
    margin: 0;
    line-height: 1.4;
  }

  .checkmark {
    position: absolute;
    top: 10px;
    left: 10px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transition: all $transition-fast;
  }

  .checkbox-input:checked ~ .checkmark {
    opacity: 1;
    background: $green-bright;
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
