<script setup>
import {useProductsStore} from "@/stores/products.js";
import {computed, reactive} from "vue";

const productStore = useProductsStore()
const form = reactive({
    brands: [],
    categories: [],
    min_price: productStore.allFilters.min_price,
    max_price: productStore.allFilters.max_price,
})

const hasPriceError = computed(() =>
    productStore.validationErrors?.field === 'price'
)

function handleSubmit() {
    productStore.loadFilteredData({...form})
}
</script>

<template>
    <div class="filter-block-inner">
        <h4>Фильтр</h4>
        <div class="filter-block">
            <span class="filter-block-line"></span>
            <h5>Категория</h5>
            <div class="filter-checkboxes" data-lenis-prevent-wheel>
                <label v-for="category in productStore.allFilters.categories" :key="category">
                    <input type="checkbox" :value="category" v-model="form.categories">
                    {{ category }}
                </label>
            </div>
        </div>

        <div class="filter-block">
            <span class="filter-block-line"></span>
            <h5>Бренд</h5>
            <div class="filter-checkboxes" data-lenis-prevent-wheel>
                <label v-for="brand in productStore.allFilters.brands" :key="brand">
                    <input type="checkbox" :value="brand" v-model="form.brands">
                    {{ brand }}
                </label>
            </div>
        </div>
        <div class="filter-block">
            <span class="filter-block-line"></span>
            <h5>Цена</h5>
            <div class="filter-checkboxes">
                <label>
                    От
                    <input
                            class="cost-input"
                            :class="{ 'cost-error': hasPriceError }"
                            type="text"
                            v-model.number="form.min_price" min="0"
                    >
                </label>
                <label>
                    До
                    <input
                            class="cost-input"
                            :class="{ 'cost-error': hasPriceError }"
                            type="text"
                            v-model.number="form.max_price" min="0"
                    >
                </label>
            </div>
        </div>
        <button class="filter-accept-btn" @click="handleSubmit">
            Применить
        </button>
    </div>
</template>

<style scoped>
.cost-error {
    border: 1px solid red !important;
}

.cost-input {
    width: 50% !important;
    height: 50% !important;
    background: transparent;
    padding: 5px 10px;
    border-width: 1px !important;
}

.filter-block-inner {
    width: 250px;
}

.filter-block {
    margin-top: 15px;
    width: 100%;
}

.filter-block-line {
    display: block;
    width: 90%;
    height: 1px;
    background: var(--color-light-gold);
    margin: 10px auto;
}

h4,
.filter-block h5 {
    font-size: clamp(16px, 1.5vw, 20px);
    font-weight: 600;
    text-transform: uppercase;
}

.filter-checkboxes {
    margin-top: min(20px, 1.5vw);
    max-height: 220px;
    overflow-y: auto;
    overscroll-behavior: contain;
    font-size: clamp(16px, 1.5vw, 20px);
    font-weight: 400;
    display: flex;
    flex-direction: column;
    gap: 15px;
    padding-left: 15px;
}

.filter-checkboxes label {
    display: inline-flex;
    align-items: center;
    gap: 20px;
}

.filter-checkboxes input {
    appearance: none;
    -webkit-appearance: none;

    width: 15px;
    height: 15px;
    border: 1px solid var(--color-light-gold);
    border-radius: 1px;
    cursor: pointer;
    position: relative;
}

.filter-checkboxes input:checked {
    background: var(--color-light-gold);
}

.filter-accept-btn {
    text-transform: none;
    margin-top: 40px;
    height: 65px;
    width: 250px;
    background-color: var(--color-gold);
    color: #251F19;
    font-weight: 600;
    font-size: 24px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--border-radius);
    border: 0;
    //box-shadow: 0 0 80px rgba(236, 223, 165, 0.8);
}

.filter-accept-btn:hover {
    //color: var(--color-gold);
    border: var(--border-hover);
    transform: scale(1.01) translateY(-5%);
}

.filter-accept-btn:active {
    transform: translateY(1%)
}

@media (max-width: 900px) {
    .filter-block-inner {
        display: none;
    }
}
</style>