<script setup>
import {useProductsStore} from "@/stores/products.js";

const productStore = useProductsStore()
</script>

<template>
    <div class="header-wrapper">
        <router-link :to="{name: 'index'}" class="header-logo">
            <img
                    src="@/assets/img/logo.png"
                    alt="DaBro logo"
                    class="header-logo-image"
                    width="174" height="63" loading="lazy"
            >
        </router-link>
        <nav class="header-menu">
            <ul class="header-menu-list">
                <li class="header-menu-item">
                    <a href="#" class="header-menu-link">У нас</a>
                </li>
                <li class="header-menu-item">
                    <a href="#" class="header-menu-link">Мастера</a>
                </li>
                <!--                <li class="header-menu-item">-->
                <!--                    <a href="/" class="header-menu-link">Услуги</a>-->
                <!--                </li>-->
                <li class="header-menu-item">
                    <router-link :to="{name: 'shop'}" class="header-menu-link">Магазин</router-link>
<!--                    <a href="#" class="header-menu-link">Галерея</a>-->
                </li>
                <li class="header-menu-item">
                    <a href="#" class="header-menu-link">Контакты</a>
                </li>
            </ul>
        </nav>
        <div class="header-actions">
            <a href="/" class="phone-number">8 912 642 20 20</a>
<!--            <a href="https://b921434.yclients.com/company/857497/select-master?o=s12564603" class="appointment-btn">Онлайн-->
<!--                запись</a>-->
            <button class="appointment-btn" @click="productStore.openSidebar()">Онлайн запись</button>
        </div>
        <button class="header-burger-button" id="burgerBtn" title="Open menu">
            <span class="visually-hidden">Open menu</span>
            <span class="header-burger-button-line"></span>
            <span class="header-burger-button-line"></span>
            <span class="header-burger-button-line"></span>
        </button>
    </div>
    <div class="header-line"></div>
</template>

<style scoped>
.header-wrapper{
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    column-gap: 20px;
    padding-inline: 32px;
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
    z-index: 10;
    /*box-sizing: content-box;*/
}

.header-logo{
    flex-shrink: 0;
}

.header-menu-list{
    display: flex;
    column-gap: 40px;
    margin: 0;
}

.header-menu-link{
    display: inline-flex;
    align-items: center;
    height: 90px;
    font-weight: 400;
    font-size: 16px;
    letter-spacing: 1.4px;
}

.header-actions{
    display: flex;
    column-gap: 25px;
}

.header-burger-button{
    flex-direction: column;
    justify-content: center;
    align-items: center;
    row-gap: 4px;
    width: 48px;
    height: 48px;
    background-color: transparent;
    border: none;
    display: none;
}

.header-burger-button-line {
    height: 2px;
    width: 22px;
    background-color: var(--color-light-gold);
}

.header-line {
    width: 100%;
    border-top: 2px solid var(--color-light-gold);
}
</style>