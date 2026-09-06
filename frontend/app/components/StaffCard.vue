<script setup>
import defaultImg from '../assets/img/staff_default.webp'

const sidebarStore = useSidebarStore()

const props = defineProps({
    staffInfo: {
        type: Object,
        required: true
    }
})
</script>

<template>
    <div class="staff-card-wrapper">
        <div class="staff-img-wrapper">
            <img :src="props.staffInfo.img_url || defaultImg"
                 alt="name photo">
            <div class="overlay">
                <p>{{ props.staffInfo?.description }}</p>
            </div>
        </div>
        <div class="staff-content-wrapper">
            <h2>{{ props.staffInfo?.name }}</h2>
            <h3>{{ props.staffInfo?.grade }}</h3>
            <button @click="sidebarStore.openBookingSidebar()">Записаться</button>
        </div>
    </div>
</template>

<style scoped>
.staff-img-wrapper {
    position: relative;
    overflow: hidden;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
}

.overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transform: translateY(20%);
    transition: transform 0.5s ease-in-out, opacity 0.5s ease-in-out;
    padding: 30px;
}

.staff-content-wrapper {
    padding: 0 15px;
}

.staff-img-wrapper img {
    transition: opacity 0.5s ease-in-out;
    filter: grayscale(100%);
    object-fit: cover;
    height: clamp(350px, 38.46vw, 500px);
    width: 100%;
}

.staff-img-wrapper:hover img {
    opacity: 0.4;
}

.staff-img-wrapper:hover .overlay {
    transform: translateY(0);
    opacity: 1;
}

.overlay p {
    font-size: 16px;
    font-weight: 400;
}

.staff-card-wrapper h2 {
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: 22px;
    font-weight: 400;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin: 20px 0;
}

.staff-card-wrapper h3 {
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: 16px;
    font-weight: 400;
    margin: 20px 0;
    text-transform: capitalize;
}

.staff-card-wrapper button {
    text-transform: none;
    margin: 30px 0;
    width: 200px;
    height: 50px;
    padding-inline: 50px;
    background-color: var(--color-gold);
    color: var(--color-black);
    font-family: var(--font-family-base), Arial, sans-serif;
    font-weight: 500;
    font-size: 20px;
    display: inline-flex;
    align-items: center;
    border: 0;
    border-radius: var(--border-radius);
    box-shadow: 0 0 20px rgba(236, 223, 165, 0.8);
}

@media (max-width: 1000px) {
    .staff-img-wrapper img {
        height: clamp(350px, 50vw, 500px);
    }
}

@media (max-width: 680px) {
    .staff-img-wrapper img {
        height: clamp(350px, 73vw, 500px);
    }
}
</style>