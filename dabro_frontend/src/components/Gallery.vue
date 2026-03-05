<script setup>

</script>

<template>
    <section class="gallery" id="gallery">
        <div class="gallery-inner container">
            <h1>галерея</h1>
            <div class="gallery-grid">
                <div class="gallery-row top-row">
                    <span class="line gallery-line-top-row top"></span>
                    <span class="line gallery-line-top-row bottom"></span>
                    <div class="gallery-item">
                        <img src="@/assets/img/gallery_s_1.png" alt="">
                    </div>
                    <div class="gallery-item">
                        <img src="@/assets/img/gallery_b_1.png" alt="">
                    </div>
                </div>
                <div class="gallery-row bottom-row">
                    <span class="line gallery-line-bottom-row top"></span>
                    <span class="line gallery-line-bottom-row bottom"></span>
                    <div class="gallery-item">
                        <img src="@/assets/img/gallery_b_2.png" alt="">
                    </div>
                    <div class="gallery-item">
                        <img src="@/assets/img/gallery_s_2.png" alt="">
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.line {
    position: absolute;
    left: -20px;
    right: -20px;
    height: 1px;
    background: var(--color-gold);
}

.gallery {
    min-height: 800px;
    width: 100%;
    padding: 100px 32px;
}

.gallery-inner h1 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-size: clamp(24px, 4.56vw, 60px);
}

.gallery-grid {
    display: grid;
    grid-template-rows: repeat(2, clamp(50px, 35.71vw, 500px));
    gap: 40px;
}

.gallery-row {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 40px;
    position: relative;
}

.gallery-item {
    z-index: 2;
}

.gallery-row::before,
.gallery-row::after {
    content: "";
    position: absolute;
    width: 1px;
    background-color: var(--color-gold);
}

.top-row::before,
.top-row::after {
    top: -5%;
    bottom: 30%;
}

.top-row::before {
    left: 66.2%;
    z-index: 1;
}

.top-row::after {
    right: -20px;
}

.bottom-row::before,
.bottom-row::after {
    top: 30%;
    bottom: -5%;
}

.bottom-row::before {
    left: -20px;
}

.bottom-row::after {
    right: 66.2%;
    z-index: 1;
}

.gallery-line-top-row {
    left: 66.2%;
    right: -20px;
}

.gallery-line-top-row.top {
    top: -5%;
}

.gallery-line-top-row.bottom {
    bottom: 30%;
}

.gallery-line-bottom-row {
    right: 66.2%;
    left: -20px;
}

.gallery-line-bottom-row.top {
    bottom: -5%;
}

.gallery-line-bottom-row.bottom {
    top: 30%;
}
</style>