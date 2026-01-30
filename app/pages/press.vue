<template>
  <div>
    <PageHero :title="$t('press.hero.title')" :subtitle="$t('press.hero.subtitle')" icon="📰" />
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
