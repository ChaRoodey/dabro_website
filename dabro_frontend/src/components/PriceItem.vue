<script setup>
defineProps({
    item: Object,
})
</script>

<template>
    <div class="price-item-wrapper">
        <div class="price-inline-wrapper">
            <h2>{{item.title}}</h2>
            <h4>{{item.price}}</h4>
        </div>
        <span class="line"></span>
        <p class="price-descr">{{item.descr}}</p>
    </div>
</template>

<style scoped>
.price-item-wrapper {
    display: flex;
    flex-direction: column;
    width: 100%;
}

.price-inline-wrapper {
    position: relative;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.line {
    height: 2px;
    width: 100%;
    background: var(--color-light-gold);
}

h2, h4 {
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: clamp(16px, 2.56vw, 22px);
    font-weight: 400;
    text-transform: uppercase;
    margin: 0;
}

p {
    font-size: clamp(10px, 1.23vw, 16px);
    font-weight: 400;
}
</style>