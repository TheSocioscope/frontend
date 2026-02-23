<template>
  <div class="products-grid">
    <div v-for="product in filteredProducts" :key="product._path" class="product-card">
      <div class="product-image">
        <img
          v-if="product.photo"
          :src="product.photo"
          :alt="product.title"
          class="product-photo"
        />
        <div v-else class="product-photo-placeholder">
          <span class="placeholder-icon">📦</span>
        </div>
      </div>
      <div class="product-content">
        <span class="product-badge">{{ product.badge }}</span>
        <h3>{{ product.title }}</h3>
        <p class="product-producer">{{ product.producer }}</p>
        <p class="product-description">{{ product.description }}</p>
        <div class="product-footer">
          <a :href="product.link" target="_blank" rel="noopener noreferrer" class="product-link">
            {{ $t('products.visitWebsite') }} <span class="external-icon">↗</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { t: $t } = useI18n()

const props = defineProps<{
  products: any[]
  activeFilter: string
}>()

const filteredProducts = computed(() => {
  if (props.activeFilter === 'all') {
    return props.products
  }
  return props.products.filter((p) => p.category === props.activeFilter)
})
</script>

<style scoped lang="scss">
@use '../../../assets/styles/variables' as *;

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2.5rem;
  margin-bottom: 3rem;

  @media (max-width: 1024px) {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }

  @media (max-width: 768px) {
    grid-template-columns: 1fr;
  }
}

.product-card {
  background: white;
  border: 2px solid $warm-beige;
  overflow: hidden;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;

  &:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 36px rgba(44, 36, 22, 0.15);
    border-color: $green-bright;
  }
}

.product-image {
  width: 100%;
  height: 250px;
  overflow: hidden;
  border-bottom: 2px solid $warm-beige;
}

.product-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;

  .product-card:hover & {
    transform: scale(1.04);
  }
}

.product-photo-placeholder {
  width: 100%;
  height: 100%;
  background: $warm-beige;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
}

.product-content {
  padding: 2rem;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.product-badge {
  display: inline-block;
  padding: 0.35rem 0.85rem;
  background: $green-bright;
  color: white;
  font-size: 0.8rem;
  font-weight: $font-weight-semibold;
  margin-bottom: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  align-self: flex-start;
  font-family: $font-family-display;
}

.product-card h3 {
  font-size: 1.6rem;
  margin-bottom: 0.75rem;
  color: $brown-dark;
  font-family: $font-family-display;
  font-weight: $font-weight-bold;
}

.product-producer {
  font-size: 0.95rem;
  color: $forest-green;
  font-weight: $font-weight-semibold;
  margin-bottom: 1rem;
  font-family: $font-family-display;
}

.product-description {
  font-size: 1.05rem;
  line-height: 1.7;
  opacity: 0.85;
  margin-bottom: 1.5rem;
  flex: 1;
  font-family: $font-family-display;
}

.product-footer {
  margin-top: auto;
}

.product-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: $green-bright;
  color: white;
  text-decoration: none;
  font-weight: $font-weight-semibold;
  transition: all 0.3s ease;
  width: 100%;
  justify-content: center;
  border: 2px solid $green-bright;
  font-family: $font-family-display;

  &:hover {
    background: $forest-green;
    border-color: $forest-green;
  }
}

.external-icon {
  font-size: 1.2rem;
}
</style>
