<template>
  <v-dialog
    :model-value="modelValue"
    transition="dialog-bottom-transition"
    max-width="520"
    scrim="rgba(0,0,0,0.4)"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card v-if="node" class="galaxy-sheet">
      <div class="sheet-header">
        <span
          class="sheet-dot"
          :style="{ background: continentColors[node.continent] || '#888' }"
        />
        <h3 class="sheet-name">{{ node.slug }}</h3>
        <v-btn
          icon="mdi-close"
          variant="text"
          density="comfortable"
          :aria-label="$t('common.close', 'Close')"
          @click="$emit('update:modelValue', false)"
        />
      </div>

      <div class="sheet-body">
        <div class="sheet-row">
          <span class="row-label">{{ $t('galaxy.sectorLabel', 'Sector') }}</span>
          <span class="row-value">{{ node.sector }}</span>
        </div>
        <div class="sheet-row">
          <span class="row-label">{{ $t('galaxy.continentLabel', 'Continent') }}</span>
          <span class="row-value">{{ node.continent }}</span>
        </div>
        <div class="sheet-row">
          <span class="row-label">{{ $t('galaxy.sizeLabel', 'Size') }}</span>
          <span class="row-value">{{ node.size }}</span>
        </div>
      </div>

      <v-card-actions class="sheet-actions">
        <v-spacer />
        <v-btn
          color="primary"
          variant="flat"
          append-icon="mdi-arrow-right"
          @click="open"
        >
          {{ $t('galaxy.openInitiative', 'Open initiative') }}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean
  node: GalaxyNode | null
  continentColors: Record<string, string>
}>()

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const { t: $t } = useI18n()
const localePath = useLocalePath()
const router = useRouter()

const open = () => {
  if (!props.node) return
  emit('update:modelValue', false)
  router.push(localePath(`/projects/${props.node.slug}`))
}
</script>

<style scoped lang="scss">
@use '~~/assets/styles/variables' as *;

.galaxy-sheet {
  background: $galaxy-sheet-bg;
  border-radius: $galaxy-sheet-radius;
  box-shadow: $galaxy-sheet-shadow;
  padding: 0;
  overflow: hidden;
}

.sheet-header {
  display: flex;
  align-items: center;
  gap: $spacing-xs;
  padding: $spacing-sm $spacing-md;
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);

  .sheet-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .sheet-name {
    flex: 1;
    margin: 0;
    font-size: 1.0625rem;
    font-weight: 600;
    color: $green-dark;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
}

.sheet-body {
  padding: $spacing-md;
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
}

.sheet-row {
  display: flex;
  justify-content: space-between;
  gap: $spacing-sm;
  font-size: 0.875rem;

  .row-label {
    color: rgba(0, 0, 0, 0.5);
    text-transform: uppercase;
    font-size: 0.6875rem;
    letter-spacing: 0.04em;
  }

  .row-value {
    color: rgba(0, 0, 0, 0.87);
    text-align: right;
  }
}

.sheet-actions {
  padding: $spacing-sm $spacing-md $spacing-md;
}
</style>
