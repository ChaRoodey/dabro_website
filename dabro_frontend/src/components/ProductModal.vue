<script setup>
import {onMounted, onUnmounted} from "vue"
import {startLenis, stopLenis} from "@/plugins/lenis.js";
import defaultImg from "@/assets/img/product_default.webp";

defineProps({
    productInfo: Object,
})

const emit = defineEmits(["close"])

onMounted(() => {
    stopLenis()
    document.body.style.overflow = "hidden"
})

onUnmounted(() => {
    startLenis()
    document.body.style.overflow = ""
})
</script>

<template>
    <div class="modal-overlay" @click.self="emit('close')">
        <div class="modal-window">
            <img :src="productInfo.img_url || defaultImg" :alt="productInfo.brand">
            <div class="modal-content">
                <h2>{{ productInfo.title }}</h2>
                <h3>{{ productInfo.brand }}</h3>
                <p class="modal-descr">{{ productInfo.description }}</p>
                <div class="inline-cost-size">
                    <p class="item-p">{{ productInfo.cost }}р/{{ productInfo.size }}</p>
                    <p class="item-p">{{ outOfStock ? 'Нет в наличии' : productInfo.items_left + 'шт' }}</p>
                </div>
                <button @click="emit('close')" class="modal-back-btn">← Назад</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(4px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;

    animation: fadeIn 0.2s ease-out;
}

.modal-window {
    position: relative;
    width: 100%;
    background: #111;
    color: var(--color-light-gold);
    max-width: 800px;
    max-height: 90vh;
    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: space-around;
    gap: 30px;
    border: 1px solid var(--color-gold);
    border-radius: 4px;
    padding: 24px;

    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);

    animation: scaleIn 0.2s ease-out;
}

.modal-content {
    flex: 0 0 60%;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    justify-content: center;
    gap: 10px;
    overflow-y: auto;
}

.modal-content h2 {
    margin-bottom: 5px;
    font-size: clamp(18px, 2.5vw, 32px);
    color: var(--color-gold);
}

.modal-content h3 {
    margin-bottom: 10px;
    font-size: clamp(16px, 2.5vw, 24px);
    color: var(--color-gold);
}

.item-p {
    font-size: clamp(16px, 2.5vw, 24px);
    font-weight: 400;
}

.modal-descr {
    font-size: 18px;
}

.inline-cost-size {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    font-size: 35px;
    align-items: center;
}

.modal-window img {
    width: 100%;
    border-radius: 4px;
    object-fit: cover;
}

.modal-back-btn {
    font-size: clamp(18px, 1.84vw, 24px);
    text-transform: uppercase;
    font-weight: 500;
    background: transparent;
    position: absolute;
    top: -40px;
    left: 0;
    z-index: 10;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes scaleIn {
    from {
        opacity: 0;
        transform: scale(0.95);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@media (max-width: 1280px) {
    .modal-window {
        width: 90%;
    }

    .modal-window img {
        width: 70%;
    }
}

@media (max-width: 680px) {
    .modal-window {
        flex-direction: column;
    }
}

</style>