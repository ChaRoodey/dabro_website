<script setup>
const sidebarStore = useSidebarStore()
</script>

<template>
    <section class="banner" id="home">
        <div class="banner-inner container">
            <div class="banner-body">
                <h1>мужской салон</h1>
                <div class="banner-mid-info">
                    <h3>Мужские стрижки и<br>бритье бороды</h3>
                    <img src="../assets/img/logo.svg" alt="DaBro logo">
                </div>
                <h2>в екатеринбурге</h2>
                <button class="banner-button desktop" @click="sidebarStore.openBookingSidebar()">
                    Записаться к мастеру
                </button>
            </div>
            <div class="banner-photo">
                <div class="banner-photo-frame">
                    <img src="../assets/img/photo_banner_v2.jpg" alt="Banner Photo">

                    <span class="line line-top"></span>
                    <span class="line line-bottom"></span>
                </div>
            </div>
            <button class="banner-button mobile" @click="sidebarStore.openBookingSidebar()">
                Записаться к мастеру
            </button>
        </div>
    </section>
</template>

<style scoped>
.banner {
    /*min-height: 800px;*/
    width: 100%;
    padding: 100px 32px;
}

.banner-inner {
    /*max-width: 1200px;*/
    margin: 0 auto;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    align-items: center;
}

.banner-body {
    text-transform: uppercase;
}

.banner-mid-info {
    display: flex;
    justify-content: center;
    align-content: center;
}

.banner-body h1,
.banner-body h2 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-size: clamp(24px, 3.4vw, 64px);
    font-weight: 700;
    margin: 10px 0;
    letter-spacing: 3px;
}

.banner-body h3 {
    font-size: clamp(16px, 1.53vw, 20px);
    text-align: right;
    text-transform: none;
    margin: 10px 10px;
}

.banner-body img {
    height: auto;
    width: clamp(130px, 17.6vw, 338px);
    padding-top: 5px;
    box-sizing: content-box;
    object-fit: contain;
}

.banner-button {
    text-transform: none;
    margin-top: 80px;
    height: 70px;
    width: 360px;
    background-color: var(--color-gold);
    color: var(--color-black);
    font-weight: 500;
    font-size: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: var(--border-radius);
    box-shadow: 0 0 80px rgba(236, 223, 165, 0.8);
}

.banner-photo {
    position: relative;
}

.banner-photo-frame {
    position: relative;
    display: inline-block;
}

.banner-photo-frame img {
    position: relative;
    display: block;
    width: clamp(200px, 35.2vw, 440px);
    max-width: 440px;
    height: auto;
    z-index: 2;
    filter: grayscale(100%);
}

.banner-photo-frame::before,
.banner-photo-frame::after {
    content: "";
    position: absolute;
    top: 40%;
    bottom: 5%;
    width: 1px;
    background-color: var(--color-gold);
}

.banner-photo-frame::before {
    left: -20px;
}

.banner-photo-frame::after {
    right: -20px;
}

.line {
    position: absolute;
    left: -20px;
    right: -20px;
    height: 1px;
    background: var(--color-gold);
}

.banner-photo-frame .line-top {
    top: 40%;
    z-index: 1;
}

.banner-photo-frame .line-bottom {
    bottom: 5%;
    z-index: 3;
}

.banner-button.mobile {
    display: none;
    margin-top: 50px;
    width: clamp(250px, 36.2vw, 362px);
}

@media (max-width: 1280px) {
    .banner {
        padding: 50px 16px;
    }
}

@media (max-width: 1000px) {
    .banner {
        padding: 40px 16px;
    }

    .banner-inner {
        flex-direction: column;
    }

    .banner-body {
        text-align: center;
    }

    .banner-button.desktop {
        display: none;
    }

    .banner-button.mobile {
        display: flex;
    }
}

@media (max-width: 680px) {
    .banner {
        padding: 20px 12px;
    }

    .banner-button.mobile {
        margin-top: 20px;
        height: 50px;
        padding-inline: 45px;
        font-size: 16px;
    }

    .banner-body h2,
    .banner-body h3 {
        margin: 5px 10px;
    }
}
</style>