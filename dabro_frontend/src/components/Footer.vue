<script setup>
import {nextTick, onBeforeUnmount, onMounted} from "vue";
import {mapDestroy, mapInit} from "@/plugins/yandexMap.js";
import iconsSprite from '@/assets/icons/icons.svg?raw'

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
        <div v-html="iconsSprite" style="display: none"/>
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
                    <div class="footer-social-media-links">
                        <a href="https://vk.com/dabro_sun">
                            <svg width="60" height="60">
                                <use href="#icon-vk"/>
                            </svg>
                        </a>
                        <a href="https://www.instagram.com/dabro_sun/">
                            <svg width="60" height="60">
                                <use href="#icon-instagram"/>
                            </svg>
                        </a>
                        <a href="https://t.me/dabro_sun">
                            <svg width="60" height="60">
                                <use href="#icon-telegram"/>
                            </svg>
                        </a>
                    </div>
                </div>
            </div>
            <div class="footer-map">
                <div id="map" style="width: 100%; height: 330px;"></div>
            </div>
        </div>

        <div class="footer-inner-mobile container">
            <div class="footer-title">
                <h1>контакты</h1>
            </div>
            <div class="contacts-inline">
                <div class="footer-contacts">
                    <div class="footer-address">
                        <h4>Адрес</h4>
                        <p>г. Екатеринбург, мкр. Солнечный<br>ул. Лучистая 6</p>
                    </div>
                    <div class="footer-phone-number">
                        <h4>Телефон</h4>
                        <a href="">8 912 642 20 20</a>
                    </div>
                    <div class="footer-working-hours">
                        <h4>Режим работы</h4>
                        <p>10:00–21:00</p>
                    </div>
                    <div class="footer-social-media">
                        <h4>Социальные сети</h4>
                        <div class="footer-social-media-links">
                            <a href="https://vk.com/dabro_sun">
                                <svg width="60" height="60">
                                    <use href="#icon-vk"/>
                                </svg>
                            </a>
                            <a href="https://www.instagram.com/dabro_sun/">
                                <svg width="60" height="60">
                                    <use href="#icon-instagram"/>
                                </svg>
                            </a>
                            <a href="https://t.me/dabro_sun">
                                <svg width="60" height="60">
                                    <use href="#icon-telegram"/>
                                </svg>
                            </a>
                        </div>
                    </div>
                </div>
                <!--                <div class="footer-logo-mobile">-->
                <!--                    <img class="mobile-footer-logo" src="@/assets/img/logo_vertical.svg" alt="ДаБро логотип">-->
                <!--                </div>-->
            </div>
            <div class="footer-map">
                <div id="mobile-map" style="width: 100%; height: 230px;"></div>
            </div>
        </div>

        <div class="footer-copyright">
            <p>© Copyright 2025-2026</p>
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

.footer-title h1 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-size: clamp(24px, 4.56vw, 60px);
    font-weight: 400;
    letter-spacing: 3px;
    margin: 0;
}

.footer-logo img {
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
    //height: 330px;
}

.footer-social-media {
    padding-right: 30px;
}

.footer-copyright {
    text-align: center;
    padding: 40px 0;
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: clamp(12px, 1.56vw, 16px);
    color: var(--color-light-gold);
}

.footer-inner-mobile {
    display: none;
    flex-direction: column;
    align-items: center;
}

.contacts-inline {
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    margin-bottom: 10px;
}

@media (max-width: 680px) {
    .footer {
        min-height: 400px;
    }

    .footer-copyright {
        padding: 10px 0;
    }

    .footer-social-media svg {
        width: 40px;
        height: 40px;
    }

    .footer-social-media-links {
        display: flex;
        justify-content: space-around;
    }
}

@media (max-width: 600px) {
    .footer {
        min-height: 0;
        padding: 50px 16px 0;
    }

    .footer-title {
        margin-bottom: 20px;
    }

    .footer-inner {
        display: none;
    }

    .footer-inner-mobile {
        display: flex;
    }

    .footer-contacts {
        align-items: center;
        text-align: center;
    }

    .footer-social-media {
        padding: 0;
    }

    .footer-copyright {
        margin-top: 10px;
    }
}
</style>