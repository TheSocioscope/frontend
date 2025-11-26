<template>
  <v-menu offset-y>
    <template #activator="{ props }">
      <v-btn color="success" variant="elevated" v-bind="props" prepend-icon="mdi-web">
        {{ currentLocale?.name }}
        <v-icon end>mdi-chevron-down</v-icon>
      </v-btn>
    </template>
    <v-list>
      <v-list-item
        v-for="loc in availableLocales"
        :key="loc.code"
        :value="loc.code"
        @click="switchLocale(loc.code)"
      >
        <v-list-item-title>{{ loc.name }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup lang="ts">
const { locale, locales, setLocale } = useI18n()
const switchLocalePath = useSwitchLocalePath()
const router = useRouter()

const availableLocales = computed(() => locales.value)
const currentLocale = computed(() => locales.value.find((l: any) => l.code === locale.value))

const switchLocale = async (newLocale: string) => {
  await setLocale(newLocale)
  const path = switchLocalePath(newLocale)
  if (path) {
    await router.push(path)
  }
}
</script>
