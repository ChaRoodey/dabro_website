<script setup>

</script>

<template>
    <section class="banner" id="home">
        <div class="banner-inner container">
            <div class="banner-body">
                <h1>мужской салон</h1>
                <div class="banner-mid-info">
                    <h3>Мужские стрижки и<br>бритье бороды</h3>
                    <img src="@/assets/img/logo_big.png" alt="DaBro logo">
                </div>
                <h2>в екатеринбурге</h2>
                <a class="banner-button desktop"
                   href="https://b921434.yclients.com/company/857497/select-master?o=s12564603">Записаться к
                    мастеру</a>
            </div>
            <div class="banner-photo">
                <div class="banner-photo-frame">
                    <img src="@/assets/img/photo_banner.png" alt="Banner Photo">

                    <span class="line line-top"></span>
                    <span class="line line-bottom"></span>
                </div>
            </div>
<!--            <a class="banner-button mobile"-->
<!--               href="https://b921434.yclients.com/company/857497/select-master?o=s12564603">Записаться к-->
<!--                мастеру</a>-->
        </div>
    </section>
</template>

<style scoped>
.banner {
    min-height: 800px;
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
    font-size: clamp(36px, 3.4vw, 64px);
    font-weight: 700;
    margin: 10px 0;
    letter-spacing: 3px;
}

.banner-body h3 {
    font-size: 20px;
    text-align: right;
    text-transform: none;
    margin: 10px 10px;
}

.banner-body img {
    height: auto;
    width: clamp(200px, 17.6vw, 338px);
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
    width: clamp(300px, 35.2vw, 440px);
    max-width: 440px;
    height: auto;
    z-index: 2;
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
</style>