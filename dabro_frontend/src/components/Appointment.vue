<script setup>
import {useProductsStore} from "@/stores/products.js";

const productStore = useProductsStore()
</script>

<template>
    <section class="appointment">
        <div class="appointment-inner container">
            <h1>запись</h1>
            <div class="appointment-content">
                <p>На услугу можно записаться онлайн или по звонку</p>
                <button class="appointment-btn-black" @click="productStore.openSidebar()">
                    Записаться онлайн
                </button>
                <a class="appointment-btn-yellow" href="tel:+79049898678">Позвонить</a>
            </div>
        </div>
    </section>
</template>

<style scoped>
.appointment {
    display: flex;
    align-items: center;
    min-height: 450px;
    width: 100%;
    background: var(--color-gold);
    color: var(--color-black);
}

.appointment-inner h1 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-size: clamp(24px, 4.56vw, 60px);
}

.appointment-content {
    display: flex;
    flex-direction: row;
    gap: 40px;
}

.appointment-content p {
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: clamp(16px, 2.56vw, 22px);
    font-weight: 400;
    text-transform: uppercase;
}

.appointment-content a,
.appointment-content button {
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: clamp(16px, 2.56vw, 20px);
    font-weight: 400;
    width: 360px;
    height: 60px;
    border-radius: 3%;
    border: 1px solid var(--color-black);
}

.appointment-btn-black {
    color: var(--color-gold);
    background-color: var(--color-black);
}

.appointment-btn-black:hover {
    background-color: var(--color-gold);
    border-color: var(--color-black);
    color: var(--color-black);
}

.appointment-btn-yellow {
    color: var(--color-black);
}

.appointment-btn-yellow:hover {
    background-color: #111111;
    border-color: var(--color-gold);
    color: var(--color-gold);
    transform: scale(1.01) translateY(-5%);
}

@media (max-width: 1000px) {
    .appointment-inner {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .appointment-content {
        flex-direction: column;
        align-items: center;
    }

    .appointment-inner {
        padding: 0 25px;
    }
}

</style>