<script setup>
import Filter from "@/components/Filter.vue";
import Catalog from "@/components/Catalog.vue";
import Footer from "@/components/Footer.vue";
import {onMounted} from "vue";
import {useProductsStore} from "@/stores/products.js";

const productStore = useProductsStore()

onMounted(() => {
    productStore.shopLoadInit()
})
</script>

<template>
    <div class="catalog-inner container">
        <h2>Магазин</h2>
        <h3>Профессиональные средства для волос, бороды и тела</h3>
        <div v-if="productStore.initLoading">
            Loading...
        </div>

        <div v-else-if="productStore.error">
            Ошибка загрузки
        </div>
        <div class="catalog-content" v-else>
            <Filter/>
            <Catalog/>
        </div>
        <Footer/>
    </div>
</template>

<style scoped>
.catalog-inner {
    max-width: 1200px;
    padding: 0 30px;
}

.catalog-content {
    display: flex;
    margin: min(60px, 3.6vw) 0;
    justify-content: space-between;
}

h2 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-size: clamp(36px, 4.9vw, 48px);
    font-weight: 700;
    margin-top: 40px;
    margin-bottom: 0;
    letter-spacing: 3px;
}

h3 {
    font-size: 20px;
    text-transform: none;
    margin-top: 10px;
}

@media (max-width: 1280px) {
    .catalog-content {
        justify-content: space-around;
    }
}
</style>