<template>
  <div>
    <ContactHero />
    <ContactForm />
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

useHead({
  title: $t('contact.meta.title'),
  meta: [
    {
      name: 'description',
      content: $t('contact.meta.description')
    }
  ]
})
</script>
