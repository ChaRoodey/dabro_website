<script setup>
import defaultImg from "@/assets/img/product_default.webp";
import {computed} from "vue";

const props = defineProps({
    productInfo: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(["select"])

const outOfStock = computed(() => {
    return props.productInfo.items_left === 0;
})

function openModal() {
    emit("select", props.productInfo)
}
</script>

<template>
    <div class="item-wrapper" @click="openModal" :class="{ 'item-wrapper--disabled': outOfStock }">
        <img :src="productInfo.img_url || defaultImg" :alt="productInfo.brand">
        <h6 class="item-title">{{ productInfo.brand }}</h6>
        <p class="item-p">{{ productInfo.title }}</p>
        <!--        <p class="item-p">{{productInfo.description}}</p>-->
        <div class="size-price-wrapper">
            <p class="item-p">{{ productInfo.cost }}р/{{ productInfo.size }}</p>
            <p class="item-p">{{ outOfStock ? 'Нет в наличии' : productInfo.items_left + 'шт' }}</p>
        </div>
    </div>
</template>

<style scoped>
.item-wrapper {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    width: 250px;
    height: 350px;
    padding: 20px 20px;
    background-color: #0b0a0a;
    transition: transform 0.3s ease;
    cursor: pointer;
    box-shadow: 0 3px 20px 0 rgba(236, 223, 165, 0.2);
}

.item-wrapper--disabled {
    opacity: 0.5;
    filter: grayscale(40%);
    //pointer-events: none;
}

.item-wrapper img {
    width: 80%;
    height: 50%;
    object-fit: cover;
    margin-bottom: 20px;
    //filter: grayscale(50%);
}

.item-wrapper:hover {
    transform: scale(1.03);
}

.item-wrapper:hover::before {
    opacity: 0.9;
}

.item-title {
    font-size: clamp(16px, 1.5vw, 20px);
    font-weight: 500;
}

.item-p {
    font-size: clamp(10px, 1.23vw, 16px);
    font-weight: 400;
}

.size-price-wrapper {
    margin-top: 10px;
    width: 100%;
    display: flex;
    justify-content: space-between;
}

@media (max-width: 1280px) {
    .item-wrapper {
        width: 230px;
        height: 300px;
    }

    .item-wrapper img {
        height: 55%;
        width: 65%;
    }
}
</style>

<!--.item-wrapper::before {-->
<!--    content: '';-->
<!--    position: absolute;-->
<!--    inset: 0;-->

<!--    background-image: var(&#45;&#45;bg-image);-->
<!--    background-size: cover;-->
<!--    background-position: center;-->
<!--    background-repeat: no-repeat;-->
<!--    filter: grayscale(80%);-->

<!--    opacity: 0.75;-->
<!--    transition: opacity 0.3s ease;-->
<!--    z-index: -1;-->
<!--}-->