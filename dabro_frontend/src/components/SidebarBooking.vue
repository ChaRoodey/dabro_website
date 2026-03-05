<script setup>
import {useProductsStore} from "@/stores/products.js";
import {ref} from "vue";

const isFrameLoaded = ref(false)
const bookingUrl = 'https://b921434.yclients.com/'
const productStore = useProductsStore()


function closeSidebar() {
    productStore.closeSidebar()
    isFrameLoaded.value = false
}
</script>

<template>
    <transition name="overlay-fade">
        <div class="sidebar-overlay" v-if="productStore.sidebarOpen" @click.self="closeSidebar">
            <transition name="sidebar-spring">
                <aside class="sidebar">
                    <button class="close" @click="closeSidebar">✕</button>

                    <div class="spinner-wrap" v-if="!isFrameLoaded">
                        <div class="spinner"></div>
                        <p class="spinner-text">Загрузка…</p>
                    </div>

                    <iframe
                            class="frame"
                            @load="isFrameLoaded = true"
                            :src="bookingUrl"
                            allowtransparency="true"
                    />
                </aside>
            </transition>
        </div>
    </transition>
</template>

<style scoped>
.sidebar-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, .55);
    backdrop-filter: blur(4px);
    z-index: 10;
}

.sidebar {
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    width: min(40%, 500px);
    border-left: 1px solid rgba(255, 255, 255, .06);
}

.close {
    position: absolute;
    top: 12px;
    left: -50px;
    z-index: 2;
    border: 1px solid #FFFFFF19;
    background: #FFFFFF0F;
    color: #fff;
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
}

.close:hover {
    transform: scale(1.03);
    background: rgba(255, 255, 255, .10);
}

.close:active {
    transform: scale(0.98);
}

.spinner-wrap {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 12px;
    background: #111;
    z-index: 2;
}

.spinner {
    width: 42px;
    height: 42px;
    border-radius: 50%;
    border: 3px solid rgba(255, 255, 255, 0.2);
    border-top-color: rgba(255, 255, 255, 0.9);
    animation: spin 0.8s linear infinite;
}

.spinner-text {
    color: rgba(255, 255, 255, 0.75);
    font-size: 14px;
    margin: 0;
}

@keyframes spin {
    to {
        transform: rotate(360deg);
    }
}

.frame {
    width: 100%;
    height: 100%;
    border: 0;
}

.overlay-fade-enter-active,
.overlay-fade-leave-active {
    transition: opacity 220ms ease;
}

.overlay-fade-enter-from,
.overlay-fade-leave-to {
    opacity: 0;
}

.overlay-fade-enter-to,
.overlay-fade-leave-from {
    opacity: 1;
}

.sidebar-spring-enter-active {
    transition: transform 520ms cubic-bezier(.16, 1, .3, 1), opacity 260ms ease;
}

.sidebar-spring-leave-active {
    transition: transform 360ms cubic-bezier(.7, 0, .84, 0), opacity 220ms ease;
}

.sidebar-spring-enter-from {
    transform: translateX(110%) rotateY(-10deg);
    opacity: 0.9;
}

.sidebar-spring-enter-to {
    transform: translateX(0) rotateY(0deg);
    opacity: 1;
}

.sidebar-spring-leave-from {
    transform: translateX(0) rotateY(0deg);
    opacity: 1;
}

.sidebar-spring-leave-to {
    transform: translateX(110%) rotateY(-8deg);
    opacity: 0.9;
}

@media (prefers-reduced-motion: reduce) {
    .overlay-fade-enter-active,
    .overlay-fade-leave-active,
    .sidebar-spring-enter-active,
    .sidebar-spring-leave-active,
    .frame {
        transition: none;
    }
}
</style>
