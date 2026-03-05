<script setup>
import {nextTick, onBeforeUnmount, onMounted} from "vue";
import {mapDestroy, mapInit} from "@/plugins/yandexMap.js";

onMounted(async () => {
    await nextTick();
    await ymaps.ready(mapInit);
})

onBeforeUnmount(() => {
    mapDestroy()
})
</script>

<template>
<footer class="footer" id="contacts">
        <div class="footer-inner container">
            <div class="footer-title">
                <h1>контакты</h1>
            </div>
            <div class="footer-logo">
                <img src="@/assets/img/dabro_logo.svg" alt="ДаБро логотип">
            </div>
            <div class="footer-contacts">
                <div class="footer-address">
                    <h4>Адрес:</h4>
                    <p>г. Екатеринбург, мкр. Солнечный, ул. Лучистая 6</p>
                </div>
                <div class="footer-phone-number">
                    <h4>Телефон:</h4>
                    <a href="">8 912 642 20 20</a>
                </div>
                <div class="footer-working-hours">
                    <h4>Режим работы:</h4>
                    <p>10:00–21:00</p>
                </div>
                <div class="footer-social-media">
                    <h4>Социальные сети</h4>
                    <a href="https://vk.com/dabro_sun">
                        <svg width="60" height="60">
<!--                            <use href="@/assets/icons/icons.svg#icon-vk"></use>-->
                        </svg>
                    </a>
                    <a href="https://www.instagram.com/dabro_sun/">
                        <svg width="60" height="60">
<!--                            <use href="@/assets/icons/icons.svg#icon-instagram"></use>-->
                        </svg>
                    </a>
                    <a href="https://t.me/dabro_sun">
                        <svg width="60" height="60">
<!--                            <use href="@/assets/icons/icons.svg#icon-telegram"></use>-->
                        </svg>
                    </a>
                </div>
            </div>
            <div class="footer-map">
                <div id="map" style="width: 100%; height: 330px;"></div>
            </div>
        </div>
        <div class="footer-copyright">
            <p>© Copyright 2025</p>
        </div>
    </footer>
</template>

<style scoped>
.footer {
    padding: 100px 32px 0;
    min-height: 700px;
    background-color: var(--color-black);
}

.footer-inner {
    display: grid;
    grid-template-columns: 1fr 1fr;
    grid-template-rows: 0.3fr 0.5fr;
    grid-row-gap: 30px;
}

.footer-title h1{
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-size: clamp(24px, 4.56vw, 60px);
    font-weight: 400;
    letter-spacing: 3px;
    margin: 0;
}

.footer-logo img{
    width: 550px;
}

.footer-contacts {
    display: flex;
    flex-direction: column;
    gap: 24px;
}

.footer-contacts h4, p {
    font-family: var(--font-family-base), Arial, sans-serif;
    font-weight: 400;
    margin: 0;
}

.footer-contacts p {
    font-size: clamp(12px, 1.56vw, 16px);
}

.footer-contacts h4 {
    font-size: clamp(16px, 2.56vw, 22px);
    text-transform: none;
}

.footer-map {
    width: 100%;
    max-width: 550px;
    height: 330px;
}

.footer-copyright {
    text-align: center;
    padding: 40px 0;
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: clamp(12px, 1.56vw, 16px);
    color: var(--color-light-gold);
}
</style>