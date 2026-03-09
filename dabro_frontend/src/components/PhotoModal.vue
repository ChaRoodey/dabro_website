<script setup>
import {ref, onBeforeUnmount, onMounted} from 'vue'
import {Cropper} from 'vue-advanced-cropper'
import 'vue-advanced-cropper/dist/style.css'

const props = defineProps({
    currPhotoUrl: String,
    objectId: [String, Number],
    instance: String,
})

const emit = defineEmits(['close', 'apply'])

const cropperRef = ref(null)

const image = ref(null)
const preview = ref(null)

const STENCIL_WIDTH = 250
const STENCIL_HEIGHT = 350
const ASPECT_RATIO = STENCIL_WIDTH / STENCIL_HEIGHT // 5 / 7

function revokeIfBlobUrl(url) {
    if (url?.startsWith?.('blob:')) {
        URL.revokeObjectURL(url)
    }
}

function onFile(e) {
    const file = e.target.files?.[0]
    if (!file) return

    if (image.value?.startsWith?.('blob:')) {
        URL.revokeObjectURL(image.value)
    }

    image.value = URL.createObjectURL(file)
    preview.value = null
}

function onReady() {
    const cropper = cropperRef.value
    if (!cropper) return

    cropper.setCoordinates({
        width: STENCIL_WIDTH,
        height: STENCIL_HEIGHT,
    })

    updatePreview()
}

function onChange() {
    updatePreview()
}

function updatePreview() {
    const cropper = cropperRef.value
    if (!cropper) return

    const canvas = cropper.getCanvas({
        width: STENCIL_WIDTH,
        height: STENCIL_HEIGHT,
    })

    preview.value = canvas ? canvas.toDataURL('image/jpeg', 0.92) : null
}

function zoomIn() {
    cropperRef.value?.zoom(1.2)
}

function zoomOut() {
    cropperRef.value?.zoom(0.8)
}

function rotateLeft() {
    cropperRef.value?.rotate(-90)
}

function rotateRight() {
    cropperRef.value?.rotate(90)
}

function resetCropper() {
    cropperRef.value?.reset()
    setTimeout(() => {
        cropperRef.value?.setCoordinates({
            width: STENCIL_WIDTH,
            height: STENCIL_HEIGHT,
        })
        updatePreview()
    }, 0)
}

function applyCrop() {
    const cropper = cropperRef.value
    if (!cropper) return

    const canvas = cropper.getCanvas({
        width: STENCIL_WIDTH,
        height: STENCIL_HEIGHT,
    })

    if (!canvas) return

    preview.value = canvas.toDataURL('image/webp', 0.92)

    canvas.toBlob((blob) => {
        if (!blob) return

        const file = new File(
            [blob],
            `cropped-${props.objectId}-${Date.now()}.webp`,
            {type: 'image/webp'}
        )

        const url = URL.createObjectURL(file)

        emit('apply', {
            id: props.objectId,
            instance: props.instance,
            file: file,
            img_url: url,
        })

        emit('close')
    }, 'image/webp', 0.92)
}

onMounted(() => {
    if (props.currPhotoUrl) image.value = props.currPhotoUrl + '?cacheBust=' + Date.now();
})

onBeforeUnmount(() => {
    revokeIfBlobUrl(image.value)
})
</script>

<template>
    <div class="modal-overlay">
        <div class="modal-window">
            <h3 class="modal-window-title">Preview</h3>
            <div class="cropper-wrapper">
                <Cropper
                        v-if="image"
                        ref="cropperRef"
                        :src="image"
                        :stencil-props="{
                        aspectRatio: ASPECT_RATIO,
                        movable: true,
                        resizable: true
                    }"
                        :canvas="true"
                        image-restriction="stencil"
                        class="cropper"
                        @ready="onReady"
                        @change="onChange"
                />

                <div v-if="preview" class="preview-wrap">
                    <p class="preview-label">250 × 350</p>
                    <img :src="preview" class="preview" alt="Preview"/>
                </div>
            </div>

            <div v-if="image" class="actions">
                <button class="modal-action-btn btn" type="button" @click="zoomIn">+</button>
                <button class="modal-action-btn btn" type="button" @click="zoomOut">-</button>
                <button class="modal-action-btn btn" type="button" @click="rotateLeft">↺</button>
                <button class="modal-action-btn btn" type="button" @click="rotateRight">↻</button>
                <button class="modal-action-btn btn" type="button" @click="resetCropper">Сбросить</button>
                <button class="modal-action-btn btn" type="button" @click="applyCrop">Применить</button>
            </div>

            <input type="file" accept="image/*" @change="onFile" class=""/>
            <button @click="emit('close')" class="modal-close-btn btn">Назад</button>
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
    max-width: 1000px;
    max-height: 90vh;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-around;
    gap: 30px;
    border: 1px solid var(--color-gold);
    border-radius: 4px;
    padding: 24px;

    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    animation: scaleIn 0.2s ease-out;
}

.modal-window-title {
    font-size: 36px;
}

.cropper-wrapper {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
}

.cropper {
    width: 100%;
    max-width: 700px;
    height: 500px;
    background: #1b1b1b;
}

.actions {
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    justify-content: center;
}

.modal-action-btn {
    min-width: 70px;
    padding: 10px 14px;
    border: 1px solid var(--color-gold);
    background: transparent;
    color: var(--color-light-gold);
    cursor: pointer;
    border-radius: 4px;
    transition: 0.3s ease;
}

.preview-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 10px;
}

.preview-label {
    margin: 0;
    font-size: 14px;
    opacity: 0.8;
}

.preview {
    width: 250px;
    height: 350px;
    object-fit: cover;
    border: 1px solid var(--color-gold);
    display: block;
}

.modal-close-btn {
    position: absolute;
    top: 20px;
    left: 20px;
    padding: 10px 16px;
    border-radius: 8px;
    border: none;
    background: var(--color-gold);
    color: #000;
    cursor: pointer;
    transition: 0.3s ease;
}

.btn:hover {
    transform: scale(1.01) translateY(-5%);
}

.btn:active {
    transform: translateY(1%)
}
</style>