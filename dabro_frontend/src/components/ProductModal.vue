<script setup>
import {onMounted, onUnmounted} from "vue"
import {startLenis, stopLenis} from "@/plugins/lenis.js";

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
    <div class="modal-overlay" @click="emit('close')">
        <div class="modal-window">
            <img :src="productInfo.img_url"/>
            <div class="modal-content">
                <h2>{{ productInfo.brand }}</h2>
                <p class="modal-descr">{{ productInfo.description }}</p>
                <div class="inline-cost-size">
                    <p>{{ productInfo.cost }}р</p>
                    <p>{{ productInfo.size }}</p>
                </div>
                <button @click="emit('close')" class="modal-close-btn">Закрыть</button>
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
    width: 100%;
    background: #111;
    color: var(--color-light-gold);
    max-width: 800px;
    max-height: 90vh;
    overflow-y: auto;
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
    gap: 10px;
}

.modal-content h2 {
    margin-bottom: 10px;
    font-size: 48px;
    color: var(--color-gold);
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

.modal-close-btn {
    margin-top: 10px;
    padding: 10px 16px;
    border-radius: 8px;
    border: none;
    background: var(--color-gold);
    color: #000;
    cursor: pointer;
    transition: background 0.2s ease;
}

.modal-close-btn:hover {
    background: var(--color-light-gold);
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
</style>