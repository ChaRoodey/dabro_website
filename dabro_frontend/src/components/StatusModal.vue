<script setup>
import {computed} from "vue";
import {useProductsStore} from "@/stores/products.js";


const props = defineProps({
    errorMessage: String,
    successMessage: String,
})

const productStore = useProductsStore()

const isError = computed(() => !!props.errorMessage)
const isSuccess = computed(() => !!props.successMessage)
const message = computed(() => props.errorMessage || props.successMessage)

const icon = computed(() => {
    if (isError.value) return '⚠'
    if (isSuccess.value) return '✓'
    return ''
})
</script>

<template>
    <div v-if="message" class="toast-wrapper">
        <div
                class="toast"
                :class="{
                'toast-error': isError,
                'toast-success': isSuccess
            }"
        >
            <span class="toast-icon">
                {{ icon }}
            </span>

            <p class="toast-message">
                {{ message }}
            </p>
        </div>
    </div>
</template>

<style scoped>
.toast-wrapper {
    position: fixed;
    top: 150px;
    right: 20px;
    z-index: 9999;
    pointer-events: none;
}

.toast {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    max-width: 360px;
    padding: 12px 16px;
    border-radius: 10px;

    backdrop-filter: blur(6px);

    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35),
    inset 0 0 0 1px rgba(255, 255, 255, 0.03);

    animation: toastIn 0.25s ease;
    pointer-events: auto;
}

/* ERROR */

.toast-error {
    background: rgba(255, 85, 85, 0.12);
    border: 1px solid rgba(255, 85, 85, 0.35);
    color: #ffb3b3;
}

/* SUCCESS */

.toast-success {
    background: rgba(60, 200, 120, 0.12);
    border: 1px solid rgba(60, 200, 120, 0.35);
    color: #b9f5c9;
}

.toast-icon {
    font-size: 18px;
    line-height: 1;
    margin-top: 1px;
}

.toast-message {
    margin: 0;
    font-size: 14px;
    line-height: 1.35;
    word-break: break-word;
}

@keyframes toastIn {
    from {
        transform: translateY(-10px);
        opacity: 0;
    }
    to {
        transform: translateY(0);
        opacity: 1;
    }
}
</style>