<template>
  <div>
    <PressHero />
    <PressResources />
    <PressQuickFacts />
    <PressContact />
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

useHead({
  title: $t('press.meta.title'),
  meta: [
    {
      name: 'description',
      content: $t('press.meta.description')
    }
  ]
})
</script>
