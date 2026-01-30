<template>
  <v-card class="project-share">
    <v-card-title class="section-title">
      <v-icon class="mr-2">mdi-share-variant-outline</v-icon>
      {{ $t('projects.detail.share') }}
    </v-card-title>
    <v-card-text>
      <div class="share-content">
        <p class="share-description">
          {{ $t('common.shareDescription') }}
        </p>

        <div class="share-buttons">
          <v-btn
            :href="facebookShareUrl"
            target="_blank"
            color="#1877F2"
            variant="flat"
            prepend-icon="mdi-facebook"
            size="large"
          >
            Facebook
          </v-btn>

          <v-btn
            :href="twitterShareUrl"
            target="_blank"
            color="#1DA1F2"
            variant="flat"
            prepend-icon="mdi-twitter"
            size="large"
          >
            Twitter
          </v-btn>

          <v-btn
            :href="linkedinShareUrl"
            target="_blank"
            color="#0A66C2"
            variant="flat"
            prepend-icon="mdi-linkedin"
            size="large"
          >
            LinkedIn
          </v-btn>

          <v-btn
            :href="emailShareUrl"
            color="#EA4335"
            variant="flat"
            prepend-icon="mdi-email"
            size="large"
          >
            Email
          </v-btn>

          <v-btn
            color="grey-darken-1"
            variant="flat"
            prepend-icon="mdi-content-copy"
            size="large"
            @click="copyLink"
          >
            {{ copied ? $t('common.copied') : $t('common.copyLink') }}
          </v-btn>
        </div>
      </div>
    </v-card-text>
  </v-card>
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

const twitterShareUrl = computed(
  () => `https://twitter.com/intent/tweet?url=${encodedUrl.value}&text=${encodedTitle.value}`
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
  margin-bottom: 2rem;
}

.section-title {
  font-size: 1.5rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  padding: 1.5rem;
  background: linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, transparent 100%);
}

.share-content {
  text-align: center;
  padding: 1rem 0;
}

.share-description {
  font-size: 1.1rem;
  color: rgba(0, 0, 0, 0.7);
  margin-bottom: 2rem;
}

.share-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
  align-items: center;
}

@media (max-width: 768px) {
  .share-buttons {
    flex-direction: column;
    width: 100%;

    .v-btn {
      width: 100%;
      max-width: 300px;
    }
  }
}
</style>
