<script setup>
import {computed} from "vue";

const props = defineProps({
    productInfo: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(["select"])
const backgroundStyle = computed(() => ({
    "--bg-image": `url(http://localhost:8000/static/products/original/${props.productInfo.img_id}.webp)`
}))

function openModal() {
    emit("select", props.productInfo)
}
</script>

<template>
    <div class="item-wrapper" :style="backgroundStyle" @click="openModal">
        <h6 class="item-title">{{productInfo.brand}}</h6>
        <p class="item-p">{{productInfo.category}}</p>
<!--        <p class="item-p">{{productInfo.description}}</p>-->
        <div class="size-price-wrapper">
            <p class="item-p">{{productInfo.cost}}р</p>
            <p class="item-p">{{productInfo.size}}</p>
        </div>
    </div>
</template>

<style scoped>
.item-wrapper {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-end;
    width: 250px;
    height: 350px;
    padding: 10px 20px;
    color: #414141;

    //overflow: hidden;
    transition: transform 0.3s ease;
    cursor: pointer;
}

.item-wrapper::before {
    content: '';
    position: absolute;
    inset: 0;

    background-image: var(--bg-image);
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;

    opacity: 0.75;
    transition: opacity 0.3s ease;
    z-index: -1;
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
</style>
