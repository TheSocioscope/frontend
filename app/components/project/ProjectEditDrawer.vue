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

            <!-- ── 1. YOUR DETAILS ─────────────────────────────────────────── -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.yourDetails') }}</h3>
              <div v-for="(contact, ci) in contacts" :key="ci" class="contact-row-wrap">
                <div class="contact-row">
                  <div class="form-group">
                    <label>{{ $t('editDrawer.name') }}<template v-if="ci === 0"> *</template></label>
                    <input
                      v-model="contact.name"
                      type="text"
                      :placeholder="$t('editDrawer.namePlaceholder')"
                    />
                  </div>
                  <div class="form-group">
                    <label>{{ $t('editDrawer.email') }}</label>
                    <input v-model="contact.email" type="email" placeholder="you@example.com" />
                  </div>
                  <div class="form-group">
                    <label>{{ $t('editDrawer.phone') }}</label>
                    <input v-model="contact.phone" type="tel" placeholder="+1 234 567 8900" />
                  </div>
                </div>
                <button v-if="ci > 0" type="button" class="contact-remove" @click="removeContact(ci)">
                  &times;
                </button>
              </div>
              <button type="button" class="add-row-btn" @click="addContact">+ Add another contact</button>
              <p class="field-hint">{{ $t('editDrawer.contactHint') }}</p>
              <p v-if="showValidation && !isValid" class="validation-error">
                {{ $t('editDrawer.validationContact') }}
              </p>
            </section>

            <div class="section-divider" />

            <!-- ── 2. INTRO ───────────────────────────────────────────────── -->
            <section class="edit-section">
              <h3 class="section-title">Intro</h3>
              <div class="form-group">
                <label>Project name</label>
                <input v-model="intro.name" type="text" />
              </div>
              <div class="form-group">
                <label>Tagline</label>
                <input v-model="intro.tagline" type="text" placeholder="Short summary sentence" />
              </div>
              <div class="form-group">
                <label>Website URL</label>
                <input v-model="intro.url" type="url" placeholder="https://" />
              </div>

              <p class="sub-header">
                <v-icon size="15">mdi-share-variant</v-icon>
                Social media
              </p>
              <div class="social-row">
                <span class="social-icon-label">
                  <v-icon size="16">mdi-instagram</v-icon>
                  Instagram
                </span>
                <input v-model="socials.instagram" type="url" placeholder="https://instagram.com/…" class="social-input" />
              </div>
              <div class="social-row">
                <span class="social-icon-label">
                  <v-icon size="16">mdi-facebook</v-icon>
                  Facebook
                </span>
                <input v-model="socials.facebook" type="url" placeholder="https://facebook.com/…" class="social-input" />
              </div>
              <div class="social-row">
                <span class="social-icon-label">
                  <v-icon size="16">mdi-linkedin</v-icon>
                  LinkedIn
                </span>
                <input v-model="socials.linkedin" type="url" placeholder="https://linkedin.com/…" class="social-input" />
              </div>
              <div class="social-row">
                <span class="social-icon-label">
                  <v-icon size="16">mdi-youtube</v-icon>
                  YouTube
                </span>
                <input v-model="socials.youtube" type="url" placeholder="https://youtube.com/…" class="social-input" />
              </div>
            </section>

            <div class="section-divider" />

            <!-- ── 3. PHOTOS & VIDEOS ─────────────────────────────────────── -->
            <section class="edit-section">
              <h3 class="section-title">Photos &amp; Videos</h3>
              <label class="media-dropzone" for="media-upload">
                <v-icon size="24" color="#4ca049">mdi-image-plus</v-icon>
                <span class="media-dropzone-text">Choose photos &amp; videos or drag &amp; drop</span>
                <span class="media-dropzone-hint">Up to 10 files · Max 20 MB each</span>
              </label>
              <input
                id="media-upload"
                type="file"
                accept="image/*,video/*"
                multiple
                class="file-input-hidden"
                @change="handleMedia"
              />
              <p v-if="mediaError" class="file-error">{{ mediaError }}</p>

              <!-- Cover Photo/Video -->
              <div v-if="mediaFiles.length" class="media-sections">
                <!-- Cover (First Item) -->
                <div class="media-cover-section">
                  <h4 class="media-section-label">
                    <v-icon size="16">{{ mediaFiles[0].file?.type?.startsWith('video/') ? 'mdi-video' : 'mdi-image' }}</v-icon>
                    Cover Photo or Video
                  </h4>
                  <div class="media-item-card media-item-featured">
                    <div class="media-item-header">
                      <div class="media-item-info">
                        <span class="media-item-name">{{ mediaFiles[0].file?.name || 'File' }}</span>
                      </div>
                      <div class="media-item-controls">
                        <button
                          v-if="mediaFiles.length > 1"
                          type="button"
                          class="reorder-btn"
                          title="Move down"
                          @click="moveMediaDown(0)"
                        >
                          <v-icon size="16">mdi-chevron-down</v-icon>
                        </button>
                        <button type="button" class="remove-btn" @click="removeMedia(0)">&times;</button>
                      </div>
                    </div>
                    <div class="form-group">
                      <label>Description (optional)</label>
                      <input
                        v-model="mediaFiles[0].description"
                        type="text"
                        placeholder="e.g. Hero image of our initiative"
                        class="media-field"
                      />
                    </div>
                    <div class="form-group">
                      <label>Date (optional)</label>
                      <input
                        v-model="mediaFiles[0].date"
                        type="text"
                        placeholder="e.g. March 15, 2023"
                        class="media-field"
                      />
                    </div>
                  </div>
                </div>

                <!-- Additional Content -->
                <div v-if="mediaFiles.length > 1" class="media-content-section">
                  <div v-for="(item, mi) in mediaFiles.slice(1)" :key="mi + 1" class="media-item-card">
                    <h4 class="media-section-label">
                      <v-icon size="16">{{ item.file?.type?.startsWith('video/') ? 'mdi-video' : 'mdi-image' }}</v-icon>
                      Content {{ mi + 2 }}
                    </h4>
                    <div class="media-item-header">
                      <div class="media-item-info">
                        <span class="media-item-name">{{ item.file?.name || 'File' }}</span>
                      </div>
                      <div class="media-item-controls">
                        <button
                          type="button"
                          class="reorder-btn"
                          title="Move up"
                          @click="moveMediaUp(mi + 1)"
                        >
                          <v-icon size="16">mdi-chevron-up</v-icon>
                        </button>
                        <button
                          v-if="mi + 1 < mediaFiles.length - 1"
                          type="button"
                          class="reorder-btn"
                          title="Move down"
                          @click="moveMediaDown(mi + 1)"
                        >
                          <v-icon size="16">mdi-chevron-down</v-icon>
                        </button>
                        <button type="button" class="remove-btn" @click="removeMedia(mi + 1)">&times;</button>
                      </div>
                    </div>
                    <div class="form-group">
                      <label>Description (optional)</label>
                      <input
                        v-model="item.description"
                        type="text"
                        placeholder="e.g. Workshop in progress"
                        class="media-field"
                      />
                    </div>
                    <div class="form-group">
                      <label>Date (optional)</label>
                      <input
                        v-model="item.date"
                        type="text"
                        placeholder="e.g. March 15, 2023"
                        class="media-field"
                      />
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <div class="section-divider" />

            <!-- ── 4. ABOUT / DESCRIPTION ─────────────────────────────────── -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.description') }}</h3>
              <textarea v-model="description" rows="8" class="edit-textarea" />
              <p class="field-hint">Tip: press Enter twice to start a new paragraph.</p>
            </section>

            <div class="section-divider" />

            <!-- ── 5. TEAM MEMBERS ────────────────────────────────────────── -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.team', 'Team members') }}</h3>
              <div v-for="(member, mi) in teamMembers" :key="mi" class="item-card">
                <button type="button" class="item-card-remove" @click="teamMembers.splice(mi, 1)">&times;</button>
                <div class="form-group">
                  <label>Name</label>
                  <input v-model="member.name" type="text" />
                </div>
                <div class="form-group">
                  <label>Role</label>
                  <input v-model="member.role" type="text" />
                </div>
                <div class="photo-upload-row">
                  <img v-if="member.preview" :src="member.preview" class="photo-thumb" alt="preview" />
                  <label :for="`team-photo-${mi}`" class="photo-upload-label">
                    <v-icon size="13">mdi-camera</v-icon>
                    {{ member.preview ? 'Change photo' : 'Add photo' }}
                  </label>
                  <input
                    :id="`team-photo-${mi}`"
                    type="file"
                    accept="image/*"
                    class="file-input-hidden"
                    @change="(e) => setItemPhoto(teamMembers, mi, e)"
                  />
                </div>
              </div>
              <button type="button" class="add-row-btn" @click="addTeamMember">+ Add team member</button>
            </section>

            <div class="section-divider" />

            <!-- ── 6. EXCHANGE BOARD — WHAT WE OFFER ─────────────────────── -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.offers') }}</h3>
              <p class="sub-header">
                <v-icon size="15">mdi-arrow-top-right</v-icon>
                What we offer
              </p>
              <div v-for="(offer, oi) in offerItems" :key="oi" class="item-card">
                <button type="button" class="item-card-remove" @click="offerItems.splice(oi, 1)">&times;</button>
                <div class="form-group">
                  <label>Name</label>
                  <input v-model="offer.name" type="text" />
                </div>
                <div class="photo-upload-row">
                  <img v-if="offer.preview" :src="offer.preview" class="photo-thumb" alt="preview" />
                  <label :for="`offer-photo-${oi}`" class="photo-upload-label">
                    <v-icon size="13">mdi-camera</v-icon>
                    {{ offer.preview ? 'Change photo' : 'Add photo' }}
                  </label>
                  <input
                    :id="`offer-photo-${oi}`"
                    type="file"
                    accept="image/*"
                    class="file-input-hidden"
                    @change="(e) => setItemPhoto(offerItems, oi, e)"
                  />
                </div>
              </div>
              <button type="button" class="add-row-btn" @click="offerItems.push({ name: '', photo: null, preview: '' })">+ Add offer</button>
            </section>

            <div class="section-divider" />

            <!-- ── 7. EXCHANGE BOARD — WHAT WE ARE LOOKING FOR ───────────── -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.lookingFor') }}</h3>
              <p class="sub-header">
                <v-icon size="15">mdi-magnify</v-icon>
                What we are looking for
              </p>
              <div v-for="(need, ni) in needItems" :key="ni" class="item-card">
                <button type="button" class="item-card-remove" @click="needItems.splice(ni, 1)">&times;</button>
                <div class="form-group">
                  <label>Name</label>
                  <input v-model="need.name" type="text" />
                </div>
                <div class="photo-upload-row">
                  <img v-if="need.preview" :src="need.preview" class="photo-thumb" alt="preview" />
                  <label :for="`need-photo-${ni}`" class="photo-upload-label">
                    <v-icon size="13">mdi-camera</v-icon>
                    {{ need.preview ? 'Change photo' : 'Add photo' }}
                  </label>
                  <input
                    :id="`need-photo-${ni}`"
                    type="file"
                    accept="image/*"
                    class="file-input-hidden"
                    @change="(e) => setItemPhoto(needItems, ni, e)"
                  />
                </div>
              </div>
              <button type="button" class="add-row-btn" @click="needItems.push({ name: '', photo: null, preview: '' })">+ Add item</button>
            </section>

            <div class="section-divider" />

            <!-- ── 8. TIMELINE — OUR JOURNEY ──────────────────────────────── -->
            <section class="edit-section">
              <h3 class="section-title">{{ $t('editDrawer.timeline') }}</h3>
              <div v-for="(entry, ei) in timelineEntries" :key="ei" class="item-card">
                <button type="button" class="item-card-remove" @click="timelineEntries.splice(ei, 1)">&times;</button>
                <div class="form-group">
                  <label>Year / Date</label>
                  <input v-model="entry.year" type="text" placeholder="e.g. 2021 or March 2021" />
                </div>
                <div class="form-group">
                  <label>Description</label>
                  <textarea v-model="entry.description" rows="3" class="edit-textarea" />
                </div>
              </div>
              <button type="button" class="add-row-btn" @click="timelineEntries.push({ year: '', description: '' })">+ Add entry</button>
            </section>

            <div class="section-divider" />

            <!-- ── 9. ADDITIONAL COMMENTS ──────────────────────────────────── -->
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

            <div class="section-divider" />

            <!-- ── 10. TERMS ACCEPTANCE ───────────────────────────────────── -->
            <section class="edit-section terms-section">
              <label class="terms-checkbox-label">
                <input v-model="termsAccepted" type="checkbox" class="terms-checkbox" />
                <span>
                  I accept the
                  <button type="button" class="terms-link" @click="showTermsModal = true">terms and conditions</button>
                </span>
              </label>
              <p v-if="showValidation && !termsAccepted" class="validation-error">
                Please accept the terms and conditions before submitting.
              </p>
            </section>
          </div>

          <!-- Terms modal -->
          <Teleport to="body">
            <Transition name="fade">
              <div v-if="showTermsModal" class="terms-modal-overlay" @click="showTermsModal = false">
                <div class="terms-modal" @click.stop>
                  <div class="terms-modal-header">
                    <h3>Terms and Conditions</h3>
                    <button type="button" class="terms-modal-close" @click="showTermsModal = false">&times;</button>
                  </div>
                  <div class="terms-modal-body">
                    <p><strong>1. Who we are.</strong> The Socioscope is a research project of the Institut d'Études Avancées de Paris (IEA), 17 quai d'Anjou, 75004 Paris, France ("we", "us"). These Terms govern your use of thesocioscope.org (the "Site"), including suggesting edits to an initiative's page and using the Exchange board. By using the Site or submitting content, you accept these Terms.</p>
                    <p><strong>2. Our role.</strong> We author and publish initiative pages. Where an initiative suggests edits, we review every suggestion and decide what to publish. Content we publish is our editorial responsibility.</p>
                    <p><strong>3. Suggesting edits to your initiative's page.</strong> You may suggest changes to the page of an initiative you represent. When you do, you agree that:</p>
                    <ul>
                      <li>the information is truthful and about your own initiative;</li>
                      <li>you will not include photos or video of people who have not agreed to appear on the Socioscope and have signed consent forms;</li>
                      <li>you will not include sensitive personal information about anyone (health, religion, ethnicity, political opinions, trade-union membership, sexual life, or similar);</li>
                      <li>you will not submit anything unlawful, misleading, defamatory, or infringing.</li>
                    </ul>
                    <p>We review suggestions before publishing and may edit, decline, or remove content that doesn't meet these Terms. Submitting a suggestion is a request to publish; it does not guarantee publication.</p>
                    <p><strong>4. Licence to the content you submit.</strong> So that we can run the Site and carry out and share our research, you grant IEA a non-exclusive, worldwide, royalty-free licence to host, store, reproduce, display, translate, adapt, and use the text, images, and other materials you submit, on the Site and in connection with the Socioscope research project, including sharing with academic research partners under data-protection agreements. This licence continues for materials already used in published research even if your page is later removed; otherwise it ends when the content is removed.</p>
                    <p><strong>5. The Exchange board.</strong> The Exchange board lets initiatives share what they offer and seek. You must not post unlawful, fraudulent, or misleading listings. We offer the board as a service; we do not vet, endorse, recommend, or facilitate any listing. We review listings before publishing and may decline or remove them.</p>
                    <p><strong>6. Acceptable use.</strong> Do not misuse the Site: no unlawful, infringing, harmful, or deceptive activity; no attempts to access accounts or data that aren't yours; no disruption of the Site.</p>
                    <p><strong>7. Intellectual property.</strong> Content we author, including researcher-documented material, belongs to IEA or its licensors and may not be reused without permission, except as the law allows.</p>
                    <p><strong>8. Disclaimers and liability.</strong> The Site is provided for research and information. To the extent permitted by French law, we make no warranties about the accuracy or completeness of initiative-supplied content and exclude liability for it.</p>
                    <p><strong>9. Data protection.</strong> We handle personal data as described in our Privacy Policy.</p>
                    <p><strong>10. Governing law.</strong> These Terms are governed by French law, and disputes fall under the competent French courts.</p>
                    <p><strong>11. Contact.</strong> thesocioscope.org@gmail.com · IEA, 17 quai d'Anjou, 75004 Paris, France.</p>
                  </div>
                  <div class="terms-modal-footer">
                    <button type="button" class="terms-accept-btn" @click="termsAccepted = true; showTermsModal = false">
                      Accept and close
                    </button>
                  </div>
                </div>
              </div>
            </Transition>
          </Teleport>

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

// ── Props ───────────────────────────────────────────────────────────────────
const props = defineProps<{
  isOpen: boolean
  project: any
  localizedName: string
  localizedDescription: string
  localizedTagline?: string
  localizedTimeline: { date: string; icon: string; text: string }[]
  localizedOffers: { title: string; icon?: string; image?: string; url?: string }[]
  localizedLookingFor: { title: string; icon?: string }[]
  pageUrl: string
}>()

const emit = defineEmits<{ close: [] }>()
const { t, locale } = useI18n()

// ── State types ─────────────────────────────────────────────────────────────
type Contact = { name: string; email: string; phone: string }
type MediaItem = { file: File | null; description: string; date: string }
type TeamMember = { name: string; role: string; photo: File | null; preview: string }
type ExchangeItem = { name: string; photo: File | null; preview: string }
type TimelineEntry = { year: string; description: string }

// ── Reactive state ──────────────────────────────────────────────────────────
const contacts = ref<Contact[]>([{ name: '', email: '', phone: '' }])
const intro = ref({ name: '', tagline: '', url: '' })
const socials = ref({ instagram: '', facebook: '', linkedin: '', youtube: '' })
const mediaFiles = ref<MediaItem[]>([])
const mediaError = ref('')
const description = ref('')
const teamMembers = ref<TeamMember[]>([])
const offerItems = ref<ExchangeItem[]>([])
const needItems = ref<ExchangeItem[]>([])
const timelineEntries = ref<TimelineEntry[]>([])
const comments = ref('')
const submitted = ref(false)
const submitting = ref(false)
const submitError = ref('')
const showValidation = ref(false)
const termsAccepted = ref(false)
const showTermsModal = ref(false)

// ── initData ─────────────────────────────────────────────────────────────────
const initData = () => {
  contacts.value = [{ name: '', email: '', phone: '' }]
  intro.value = {
    name: props.localizedName || '',
    subtitle: (props.project as any)?.entityDescription || '',
    tagline: props.localizedTagline || '',
    url: (props.project as any)?.url || '',
  }
  socials.value = { instagram: '', facebook: '', linkedin: '', youtube: '' }
  mediaFiles.value = []
  mediaError.value = ''
  description.value = props.localizedDescription || ''
  teamMembers.value = ((props.project as any)?.team || []).map((m: any) => ({
    name: [m.firstname, m.lastname].filter(Boolean).join(' ') || m.name || '',
    role: m.role || '',
    photo: null,
    preview: '',
  }))
  offerItems.value = (props.localizedOffers || []).map((o) => ({
    name: o.title || '',
    photo: null,
    preview: '',
  }))
  needItems.value = (props.localizedLookingFor || []).map((l) => ({
    name: l.title || '',
    photo: null,
    preview: '',
  }))
  timelineEntries.value = (props.localizedTimeline || []).map((e) => ({
    year: e.date || '',
    description: e.text || '',
  }))
  comments.value = ''
  submitted.value = false
  termsAccepted.value = false
  submitError.value = ''
  showValidation.value = false
}

watch(
  () => props.isOpen,
  (open) => {
    if (open) initData()
  },
)

// ── Contact helpers ──────────────────────────────────────────────────────────
const addContact = () => contacts.value.push({ name: '', email: '', phone: '' })
const removeContact = (i: number) => contacts.value.splice(i, 1)

// ── Team member helper ───────────────────────────────────────────────────────
const addTeamMember = () =>
  teamMembers.value.push({ name: '', role: '', photo: null, preview: '' })

// ── Per-item photo helper ────────────────────────────────────────────────────
const setItemPhoto = (
  list: Ref<{ photo: File | null; preview: string }[]>,
  index: number,
  e: Event,
) => {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  list.value[index].photo = file
  list.value[index].preview = URL.createObjectURL(file)
}

// ── Media upload handler ─────────────────────────────────────────────────────
const handleMedia = (e: Event) => {
  const files = Array.from((e.target as HTMLInputElement).files || [])
  const MAX_MB = 20
  const skipped: string[] = []
  const valid = files.filter((f) => {
    if (f.size > MAX_MB * 1024 * 1024) {
      skipped.push(f.name)
      return false
    }
    return true
  })
  const newItems = valid.map((file) => ({
    file,
    description: '',
    date: '',
  }))
  const combined = [...mediaFiles.value, ...newItems].slice(0, 10)
  mediaFiles.value = combined
  mediaError.value = skipped.length ? `Skipped (too large): ${skipped.join(', ')}` : ''
  ;(e.target as HTMLInputElement).value = ''
}

const removeMedia = (i: number) => {
  mediaFiles.value.splice(i, 1)
  if (!mediaFiles.value.length) mediaError.value = ''
}

const moveMediaUp = (i: number) => {
  if (i > 0) {
    const temp = mediaFiles.value[i]
    mediaFiles.value[i] = mediaFiles.value[i - 1]
    mediaFiles.value[i - 1] = temp
  }
}

const moveMediaDown = (i: number) => {
  if (i < mediaFiles.value.length - 1) {
    const temp = mediaFiles.value[i]
    mediaFiles.value[i] = mediaFiles.value[i + 1]
    mediaFiles.value[i + 1] = temp
  }
}

// ── Validation ───────────────────────────────────────────────────────────────
const isValid = computed(
  () =>
    contacts.value[0].name.trim() &&
    (contacts.value[0].email.trim() || contacts.value[0].phone.trim()),
)

// ── buildEmailBody ────────────────────────────────────────────────────────────
const buildEmailBody = (): string => {
  const proj = props.project as any
  const lines: string[] = []

  lines.push(`Project: ${intro.value.name} (#${proj?.pubId ?? ''})`)
  lines.push(`Page: ${props.pageUrl}`)
  lines.push(`Language edited: ${locale.value}`)
  lines.push('')

  // Contacts
  lines.push('--- CONTACTS ---')
  contacts.value.forEach((c, i) => {
    lines.push(`Contact ${i + 1}:`)
    if (c.name) lines.push(`  Name: ${c.name}`)
    if (c.email) lines.push(`  Email: ${c.email}`)
    if (c.phone) lines.push(`  Phone: ${c.phone}`)
  })
  lines.push('')

  // Intro
  lines.push('--- INTRO ---')
  lines.push(`Project name: ${intro.value.name}`)
  lines.push(`Tagline: ${intro.value.tagline}`)
  lines.push(`Website URL: ${intro.value.url}`)
  lines.push('')

  // Social media
  const socialEntries = Object.entries(socials.value).filter(([, v]) => v.trim())
  if (socialEntries.length) {
    lines.push('--- SOCIAL MEDIA ---')
    socialEntries.forEach(([platform, url]) => lines.push(`  ${platform}: ${url}`))
    lines.push('')
  }

  // Media files
  if (mediaFiles.value.length) {
    lines.push('--- PHOTOS & VIDEOS ---')
    mediaFiles.value.forEach((item, i) => {
      const filename = item.file?.name || 'File'
      const descText = item.description ? ` — ${item.description}` : ''
      const dateText = item.date ? ` (${item.date})` : ''
      lines.push(`  ${i + 1}. ${filename}${descText}${dateText}`)
    })
    lines.push('Note: Media files attached in email')
    lines.push('')
  }

  // Description
  if (description.value.trim()) {
    lines.push('--- DESCRIPTION ---')
    lines.push(description.value.trim())
    lines.push('')
  }

  // Team members
  if (teamMembers.value.length) {
    lines.push('--- TEAM MEMBERS ---')
    teamMembers.value.forEach((m, i) => {
      lines.push(`  ${i + 1}. ${m.name}${m.role ? ` — ${m.role}` : ''}${m.photo ? ' [photo attached]' : ''}`)
    })
    lines.push('')
  }

  // Offers
  if (offerItems.value.length) {
    lines.push('--- WHAT WE OFFER ---')
    offerItems.value.forEach((o, i) => {
      lines.push(`  ${i + 1}. ${o.name}${o.photo ? ' [photo attached]' : ''}`)
    })
    lines.push('')
  }

  // Looking for
  if (needItems.value.length) {
    lines.push('--- WHAT WE ARE LOOKING FOR ---')
    needItems.value.forEach((n, i) => {
      lines.push(`  ${i + 1}. ${n.name}${n.photo ? ' [photo attached]' : ''}`)
    })
    lines.push('')
  }

  // Timeline
  if (timelineEntries.value.length) {
    lines.push('--- TIMELINE ---')
    timelineEntries.value.forEach((e) => {
      lines.push(`  [${e.year}] ${e.description}`)
    })
    lines.push('')
  }

  // Comments
  if (comments.value.trim()) {
    lines.push('--- ADDITIONAL COMMENTS ---')
    lines.push(comments.value.trim())
  }

  return lines.join('\n')
}

// ── handleSubmit ──────────────────────────────────────────────────────────────
const handleSubmit = async () => {
  showValidation.value = true
  if (!isValid.value || !termsAccepted.value) return

  submitting.value = true
  submitError.value = ''

  try {
    const proj = props.project as any
    const formData = new FormData()
    formData.append('access_key', web3formsKey)
    formData.append('to', 'thesocioscope.org@gmail.com')
    formData.append('subject', `Edit suggestion — ${intro.value.name} (#${proj?.pubId ?? ''})`)
    formData.append('from_name', contacts.value[0].name)
    formData.append('email', contacts.value[0].email || 'thesocioscope.org@gmail.com')
    if (contacts.value[0].email) formData.append('replyto', contacts.value[0].email)
    formData.append('message', buildEmailBody())

    // Media files with metadata
    mediaFiles.value.forEach((item, i) => {
      if (item.file) {
        formData.append('attachment[]', item.file, item.file.name)
        if (item.description) formData.append(`media_description_${i}`, item.description)
        if (item.date) formData.append(`media_date_${i}`, item.date)
      }
    })

    // Team photos
    teamMembers.value.forEach((m, i) => {
      if (m.photo) formData.append(`team_photo_${i}`, m.photo, m.photo.name)
    })

    // Offer photos
    offerItems.value.forEach((o, i) => {
      if (o.photo) formData.append(`offer_photo_${i}`, o.photo, o.photo.name)
    })

    // Need photos
    needItems.value.forEach((n, i) => {
      if (n.photo) formData.append(`need_photo_${i}`, n.photo, n.photo.name)
    })

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

  const SR = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition
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
  color: white;
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

.section-title {
  font-size: 0.95rem;
  font-weight: 700;
  color: $brown-dark;
  margin: 0 0 0.75rem;
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

  input,
  textarea {
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
}

.edit-input,
.edit-textarea {
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

// ── Contact rows ────────────────────────────────────────────────────────────
.contact-row-wrap {
  position: relative;
  margin-bottom: 8px;
}

.contact-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 8px;
  align-items: end;

  @media (max-width: 480px) {
    grid-template-columns: 1fr;
  }
}

.contact-remove {
  position: absolute;
  top: 0;
  right: -20px;
  background: none;
  border: none;
  font-size: 1.1rem;
  color: $brown-medium;
  cursor: pointer;
  line-height: 1;
  padding: 0;

  &:hover {
    color: #c0392b;
  }

  @media (max-width: 540px) {
    position: static;
    display: block;
    margin-top: 4px;
    text-align: right;
  }
}

// ── Ghost add-row button ───────────────────────────────────────────────────
.add-row-btn {
  display: flex;
  align-items: center;
  justify-content: center;
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
  transition: border-color $transition-fast, color $transition-fast;
  margin-top: 4px;

  &:hover {
    border-color: $green-bright;
    color: $green-bright;
  }
}

// ── Social rows ────────────────────────────────────────────────────────────
.social-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.social-icon-label {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 110px;
  font-size: 0.82rem;
  color: $brown-dark;
  font-weight: 600;
  flex-shrink: 0;
}

.social-input {
  flex: 1;
  padding: 0.5rem 0.75rem;
  border: 1.5px solid $border-cream;
  border-radius: $border-radius-md;
  font-size: 0.88rem;
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

// ── Sub-header ─────────────────────────────────────────────────────────────
.sub-header {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 10px;
  margin-top: 16px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: $green-forest;
}

// ── Item cards (team, offer, need, timeline) ───────────────────────────────
.item-card {
  position: relative;
  border: 1px solid $border-cream;
  border-radius: $border-radius-md;
  padding: 0.75rem;
  margin-bottom: 0.5rem;
  background: $cream-dark;

  .form-group {
    margin-bottom: 0.6rem;

    &:last-child {
      margin-bottom: 0;
    }
  }
}

.item-card-remove {
  position: absolute;
  top: 6px;
  right: 8px;
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  color: $brown-medium;
  line-height: 1;
  padding: 0;

  &:hover {
    color: #c0392b;
  }
}

// ── Photo upload inline ────────────────────────────────────────────────────
.photo-upload-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 6px;
}

.photo-thumb {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid $border-cream;
  flex-shrink: 0;
}

.photo-upload-label {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.78rem;
  color: $green-bright;
  cursor: pointer;
  border: 1px solid $green-bright;
  border-radius: $border-radius-pill;
  padding: 3px 10px;
  transition: all $transition-fast;

  &:hover {
    background: rgba(76, 160, 73, 0.08);
  }
}

// ── Media drop zone ────────────────────────────────────────────────────────
.media-dropzone {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  border: 1.5px dashed $border-cream;
  border-radius: $border-radius-md;
  padding: 1.25rem;
  text-align: center;
  cursor: pointer;
  transition: all $transition-fast;
  background: $cream-dark;

  &:hover {
    border-color: $green-bright;
    background: rgba(76, 160, 73, 0.04);
  }
}

.media-dropzone-text {
  font-size: 0.85rem;
  color: $brown-medium;
  font-weight: 500;
}

.media-dropzone-hint {
  font-size: 0.75rem;
  color: $text-caption;
}

.media-chips {
  display: flex;
  flex-direction: column;
  gap: 4px;
  margin-top: 0.5rem;
}

.media-chip {
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

.media-chip-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

// ── Shared file helpers ────────────────────────────────────────────────────
.file-input-hidden {
  display: none;
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

// ── Media sections ────────────────────────────────────────────────────────
.media-sections {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-top: 0.75rem;
}

.media-cover-section,
.media-content-section {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.media-section-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: $green-forest;
  margin: 0;
  padding: 0.5rem 0;
  border-bottom: 1px solid $border-cream;
}

.media-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 0.75rem;
}

.media-item-card {
  border: 1px solid $border-cream;
  border-radius: $border-radius-md;
  padding: 0.75rem;
  background: $cream-dark;

  &.media-item-featured {
    border: 2px solid $green-forest;
    background: rgba(76, 160, 73, 0.04);
    padding: 1rem;
  }
}

.media-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.media-item-info {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: 1;
  min-width: 0;
}

.media-item-name {
  flex: 1;
  font-size: 0.82rem;
  color: $brown-dark;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.media-item-controls {
  display: flex;
  align-items: center;
  gap: 4px;
  flex-shrink: 0;
}

.reorder-btn {
  background: white;
  border: 1px solid $border-cream;
  border-radius: $border-radius-sm;
  width: 28px;
  height: 28px;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: $brown-medium;
  transition: all $transition-fast;
  flex-shrink: 0;

  &:hover {
    border-color: $green-bright;
    color: $green-bright;
    background: rgba(76, 160, 73, 0.04);
  }
}

.remove-btn {
  background: none;
  border: none;
  color: $brown-medium;
  cursor: pointer;
  font-size: 1rem;
  line-height: 1;
  padding: 0;
  flex-shrink: 0;
  transition: color $transition-fast;

  &:hover {
    color: #c0392b;
  }
}

.media-field {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1.5px solid $border-cream;
  border-radius: $border-radius-md;
  font-size: 0.85rem;
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

.terms-section {
  padding-bottom: 0.5rem;
}

.terms-checkbox-label {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  font-size: 0.9rem;
  color: $text-primary;
  cursor: pointer;
  line-height: 1.5;
}

.terms-checkbox {
  margin-top: 2px;
  flex-shrink: 0;
  width: 16px;
  height: 16px;
  accent-color: $green-leaf;
  cursor: pointer;
}

.terms-link {
  background: none;
  border: none;
  padding: 0;
  color: $green-forest;
  font-size: inherit;
  font-family: inherit;
  font-weight: 600;
  text-decoration: underline;
  cursor: pointer;

  &:hover {
    color: $green-leaf;
  }
}

.terms-modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(44, 36, 22, 0.55);
  z-index: 10000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.terms-modal {
  background: white;
  border-radius: 10px;
  width: 100%;
  max-width: 640px;
  max-height: 85dvh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 12px 48px rgba(0, 0, 0, 0.22);
}

.terms-modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 24px 14px;
  border-bottom: 1px solid $border-soft;
  flex-shrink: 0;

  h3 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 700;
    color: $green-forest;
    font-family: $font-family-display;
  }
}

.terms-modal-close {
  background: none;
  border: none;
  font-size: 1.4rem;
  line-height: 1;
  color: $text-secondary;
  cursor: pointer;
  padding: 2px 6px;
  border-radius: 4px;

  &:hover {
    background: $earth-5;
    color: $text-primary;
  }
}

.terms-modal-body {
  overflow-y: auto;
  padding: 20px 24px;
  flex: 1;
  font-size: 0.875rem;
  line-height: 1.7;
  color: $text-primary;

  p {
    margin: 0 0 0.85rem;
  }

  ul {
    margin: 0.25rem 0 0.85rem 1.5rem;
    padding: 0;

    li {
      margin-bottom: 0.35rem;
    }
  }

  strong {
    color: $green-forest;
  }
}

.terms-modal-footer {
  padding: 14px 24px 18px;
  border-top: 1px solid $border-soft;
  flex-shrink: 0;
  display: flex;
  justify-content: flex-end;
}

.terms-accept-btn {
  background: $green-leaf;
  color: white;
  border: none;
  padding: 10px 22px;
  font-size: 0.9rem;
  font-weight: 600;
  font-family: $font-family-base;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.15s;

  &:hover {
    background: $green-leaf-dark;
  }
}

@keyframes pulse {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.6;
  }
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
