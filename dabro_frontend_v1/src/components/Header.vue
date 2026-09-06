<script setup>
import {useProductsStore} from "@/stores/products.js";
import {getLenis} from "@/plugins/lenis.js";
import router from "@/router/index.js";
import {useRoute} from "vue-router";
import {ref} from "vue";
import iconsSprite from '@/assets/icons/icons.svg?raw'
import MobileMenu from "@/components/MobileMenu.vue";

const productStore = useProductsStore()
const route = useRoute()
const isMobileMenuOpened = ref(false)

async function goToSection(target) {
    if (route.name !== 'index') {
        await router.push({
            name: 'index',
            query: {scroll: target.replace('#', '')}
        })
        return
    }

    const lenis = getLenis()
    if (!lenis) return

    lenis.scrollTo(target, {offset: -100})
}

function openMobileSidebar() {
    isMobileMenuOpened.value = true;
}

function closeMobileSidebar(option) {
    isMobileMenuOpened.value = false;
    if (option) goToSection(option)
}
</script>

<template>
    <header class="header">
        <div class="header-wrapper">
            <router-link :to="{name: 'index'}" class="header-logo">
                <img
                        src="@/assets/img/logo.svg"
                        alt="DaBro logo"
                        class="header-logo-image"
                        width="174" height="63" loading="lazy"
                >
            </router-link>
            <nav class="header-menu">
                <ul class="header-menu-list">
                    <li class="header-menu-item">
                        <a href="" @click.prevent="goToSection('#staff')" class="header-menu-link">Мастера</a>
                    </li>
                    <li class="header-menu-item">
                        <a href="" @click.prevent="goToSection('#price')" class="header-menu-link">Услуги</a>
                    </li>
                    <li class="header-menu-item">
                        <router-link :to="{name: 'shop'}" class="header-menu-link">Магазин</router-link>
                    </li>
                </ul>
            </nav>
            <div class="header-actions">
                <a href="tel:+79126422020" class="phone-number">8 912 642 20 20</a>
                <button class="appointment-btn" @click="productStore.openSidebar()">Онлайн запись</button>
            </div>
            <button class="header-burger-button" title="Open menu" @click="openMobileSidebar">
                <span class="visually-hidden">Open menu</span>
                <span class="header-burger-button-line"></span>
                <span class="header-burger-button-line"></span>
                <span class="header-burger-button-line"></span>
            </button>

            <MobileMenu
                    v-if="isMobileMenuOpened"
                    @staffLink="closeMobileSidebar('#staff')"
                    @priceLink="closeMobileSidebar('#price')"
                    @close="closeMobileSidebar"
            />
        </div>
        <div class="header-line"></div>
    </header>
</template>

<style scoped>
.header {
    position: sticky;
    top: 0;
    background: var(--color-black);
    z-index: 9;
}

.header-wrapper {
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

.header-logo {
    flex-shrink: 0;
}

.header-menu-list {
    display: flex;
    column-gap: 70px;
    margin: 0;
}

.header-menu-link {
    display: inline-flex;
    align-items: center;
    height: 90px;
    font-weight: 400;
    font-size: 16px;
    letter-spacing: 1.4px;
}

.header-actions {
    display: flex;
    column-gap: 25px;
}

.header-burger-button {
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

@media (max-width: 1280px) {
    .header-wrapper {
        flex-wrap: wrap;
        row-gap: 10px;
        padding: 20px 0;
        padding-inline: 15px;
    }

    .header-menu {
        order: 1;
        flex-basis: 100%;
    }

    .header-menu-link {
        height: 50px;
    }

    .phone-number {
        padding-inline: 15px;
    }
}

@media (max-width: 680px) {
    .header-logo {
        padding-left: 25px;
    }

    .header-menu {
        display: none;
    }

    .header-burger-button {
        display: inline-flex;
    }

    .header-line {
        top: 90px;
    }

}

@media (max-width: 480px) {
    .phone-number {
        display: none;
    }
}
</style>