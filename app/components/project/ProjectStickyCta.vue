<template>
  <div class="project-sticky-cta">
    <v-btn
      color="success"
      size="large"
      block
      prepend-icon="mdi-account-plus-outline"
      @click="emit('connect')"
    >
      {{ $t('common.connectButton') }}
    </v-btn>
  </div>
</template>

<script setup lang="ts">
const emit = defineEmits<{ connect: [] }>()
const { t: $t } = useI18n()
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.project-sticky-cta {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 50;
  padding: $rhythm-1 $gutter-mobile;
  background: white;
  border-top: 1px solid $border-soft;
  box-shadow: 0 -4px 16px rgba(0, 0, 0, 0.06);

  // Desktop carries the Connect CTA in the sidebar; the bottom bar
  // is for tablet + mobile only.
  @media (min-width: $detail-bp-desktop) {
    display: none;
  }
}
</style>
