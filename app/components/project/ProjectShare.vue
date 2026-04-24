<template>
  <div class="project-share">
    <span class="share-label">{{ $t('projects.detail.share') }}:</span>
    <div class="share-buttons">
      <v-btn
        :href="facebookShareUrl"
        target="_blank"
        color="#1877F2"
        variant="flat"
        prepend-icon="mdi-facebook"
        size="small"
      >
        Facebook
      </v-btn>

      <v-btn
        :href="linkedinShareUrl"
        target="_blank"
        color="#0A66C2"
        variant="flat"
        prepend-icon="mdi-linkedin"
        size="small"
      >
        LinkedIn
      </v-btn>

      <v-btn
        :href="emailShareUrl"
        color="#EA4335"
        variant="flat"
        prepend-icon="mdi-email"
        size="small"
      >
        Email
      </v-btn>

      <v-btn
        color="grey-darken-1"
        variant="flat"
        prepend-icon="mdi-content-copy"
        size="small"
        @click="copyLink"
      >
        {{ copied ? $t('common.copied') : $t('common.copyLink') }}
      </v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  projectName: string
  projectUrl: string
}>()

const { t: $t } = useI18n()
const copied = ref(false)

const encodedUrl = computed(() => encodeURIComponent(props.projectUrl))
const encodedTitle = computed(() => encodeURIComponent(props.projectName))

const facebookShareUrl = computed(
  () => `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl.value}`
)

const linkedinShareUrl = computed(
  () => `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl.value}`
)

const emailShareUrl = computed(
  () => `mailto:?subject=${encodedTitle.value}&body=${encodedUrl.value}`
)

const copyLink = async () => {
  try {
    await navigator.clipboard.writeText(props.projectUrl)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>

<style scoped lang="scss">
.project-share {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 2rem;
  padding: 1rem 0;
  border-top: 1px solid rgba(0, 0, 0, 0.08);
}

.share-label {
  font-size: 0.95rem;
  font-weight: 600;
  color: rgba(0, 0, 0, 0.7);
  white-space: nowrap;
}

.share-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

@media (max-width: 600px) {
  .project-share {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
