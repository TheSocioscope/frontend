<template>
  <div class="products-grid">
    <a
      v-for="product in filteredProducts"
      :key="product._path"
      :href="product.link"
      target="_blank"
      rel="noopener noreferrer"
      class="product-card"
    >
      <div class="product-image">
        <img
          v-if="product.photo"
          :src="product.photo"
          :alt="product.title"
          class="product-photo"
        />
        <div v-else class="product-photo-placeholder">
          <span class="placeholder-icon" aria-hidden="true">📦</span>
        </div>
        <span v-if="product.badge" class="product-badge">{{ product.badge }}</span>
      </div>
      <div class="product-content">
        <div class="product-heading">
          <h3>{{ product.title }}</h3>
          <span class="product-arrow" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="14" height="14">
              <path
                d="M5 12h14M13 6l6 6-6 6"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
                stroke-linejoin="round"
              />
            </svg>
          </span>
        </div>
        <p v-if="product.producer" class="product-producer">{{ product.producer }}</p>
        <p v-if="product.description" class="product-description">{{ product.description }}</p>
      </div>
    </a>
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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;

  /* Mobile: 2-up tile grid (matches the team page aesthetic). */
  @media (max-width: 600px) {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.75rem;
  }
}

/* The whole card is the link — sleeker than a separate "Visit website"
   button at the bottom of every card. Hover state lifts the card and
   fills the arrow chip with green, matching the team + partners pattern. */
.product-card {
  background: white;
  border: 1px solid $cream-dark;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  text-decoration: none;
  color: inherit;
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;

  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(44, 36, 22, 0.08);
    border-color: $green-bright;

    .product-photo {
      transform: scale(1.03);
    }
    .product-arrow {
      background: $green-bright;
      border-color: $green-bright;
      color: white;
    }
  }

  &:focus-visible {
    outline: 2px solid $green-bright;
    outline-offset: 2px;
  }
}

.product-image {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 10;
  overflow: hidden;
  border-bottom: 1px solid $cream-dark;
}

.product-photo {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.4s ease;
}

.product-photo-placeholder {
  width: 100%;
  height: 100%;
  background: $warm-beige;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
}

/* Badge floats over the top-left of the image — frees up vertical room
   in the content column. */
.product-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 0.25rem 0.625rem;
  background: rgba(255, 255, 255, 0.94);
  color: $forest-green;
  font-size: 0.6875rem;
  font-weight: $font-weight-semibold;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-radius: 999px;
  font-family: $font-family-display;
  backdrop-filter: blur(2px);
}

.product-content {
  padding: 1rem 1.125rem 1.125rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;

  @media (max-width: 600px) {
    padding: 0.625rem 0.75rem 0.875rem;
  }
}

.product-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.125rem;
}

.product-card h3 {
  font-size: 1.0625rem;
  margin: 0;
  color: $brown-dark;
  font-family: $font-family-display;
  font-weight: 600;
  line-height: 1.3;
  flex: 1;
  min-width: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;

  @media (max-width: 600px) {
    font-size: 0.9375rem;
  }
}

.product-arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  flex-shrink: 0;
  border: 1px solid rgba(44, 36, 22, 0.2);
  border-radius: 4px;
  color: $brown-dark;
  transition: background 0.2s ease, color 0.2s ease, border-color 0.2s ease;

  @media (max-width: 600px) {
    width: 24px;
    height: 24px;
  }
}

.product-producer {
  font-size: 0.8125rem;
  color: $forest-green;
  font-weight: $font-weight-semibold;
  margin: 0;
  font-family: $font-family-display;

  @media (max-width: 600px) {
    font-size: 0.75rem;
  }
}

.product-description {
  font-size: 0.875rem;
  line-height: 1.5;
  color: $brown-dark;
  opacity: 0.78;
  margin: 0.25rem 0 0;
  font-family: $font-family-display;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;

  /* On a 2-up phone grid, 3 lines of body would stretch each card too
     tall. Cap to 2 so the row heights stay tight. */
  @media (max-width: 600px) {
    font-size: 0.75rem;
    line-height: 1.45;
    -webkit-line-clamp: 2;
  }
}
</style>
