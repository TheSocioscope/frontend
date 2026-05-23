<template>
  <ul class="galaxy-a11y-list" :aria-label="$t('galaxy.a11yLabel', 'All initiatives in the galaxy')">
    <li v-for="node in nodes" :key="node.id">
      <NuxtLink :to="localePath(`/projects/${node.slug}`)">
        {{ node.slug }}
      </NuxtLink>
    </li>
  </ul>
</template>

<script setup lang="ts">
defineProps<{
  nodes: GalaxyNode[]
}>()

const { t: $t } = useI18n()
const localePath = useLocalePath()
</script>

<style scoped lang="scss">
// Visually hidden but reachable by screen readers + tab navigation.
.galaxy-a11y-list {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
  list-style: none;
}
</style>
