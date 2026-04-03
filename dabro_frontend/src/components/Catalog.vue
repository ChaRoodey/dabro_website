<script setup>
import CatalogItem from "@/components/CatalogItem.vue";
import {useProductsStore} from "@/stores/products.js";
import {ref} from "vue";
import ProductModal from "@/components/ProductModal.vue";

const productStore = useProductsStore()

const selectedProduct = ref(null);

function handleSelect(product) {
    selectedProduct.value = product
}

function handleClose() {
    selectedProduct.value = null
}
</script>

<template>
    <div class="catalog-content-inner">
        <router-link :to="{name: 'index'}" class="catalog-back-btn">← Назад</router-link>
        <div class="catalog-list">
            <CatalogItem
                    v-for="item in productStore.allProducts"
                    :key="item.product_id"
                    :productInfo="item"
                    @select="handleSelect"
            />
        </div>

        <div class="catalog-btn-wrapper" v-if="productStore.allProducts.length >= 10">
            <button class="catalog-list-load-more-btn">Показать ещё</button>
        </div>

        <ProductModal
                v-if="selectedProduct"
                :productInfo="selectedProduct"
                @close="handleClose"
        />
    </div>
</template>

<style scoped>
.catalog-content-inner {
    display: flex;
    flex-direction: column;
    //align-items: center;
    gap: 25px;
}

.catalog-back-btn {
    font-size: clamp(18px, 1.84vw, 24px);
    text-transform: uppercase;
    font-weight: 500;
}

.catalog-list {
    margin-top: 15px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 35px;
}

.catalog-btn-wrapper {
    width: 100%;
    display: inline-flex;
    justify-content: center;
}

.catalog-list-load-more-btn {
    //width: 20%;
    color: var(--color-light-gold);
    background-color: transparent;
    border: var(--border);
    border-radius: var(--border-radius);
    font-size: 20px;
    padding: 15px 30px;
    transition: 0.3s ease;
}

.catalog-list-load-more-btn:hover {
    color: var(--color-gold);
    border: var(--border-hover);
    transform: scale(1.01) translateY(-5%);
}

.catalog-list-load-more-btn:active {
    transform: translateY(1%)
}

@media (max-width: 1280px) {
    .catalog-list {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (max-width: 680px) {
    .catalog-content-inner {
        margin-top: 30px;
    }

    .catalog-list {
        grid-template-columns: repeat(1, 1fr);
    }
}
</style>