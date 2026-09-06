<script setup>
const sidebarStore = useSidebarStore()
const emit = defineEmits(['close', 'staffLink', 'priceLink'])

function closeSidebar() {
    emit('close')
}
</script>

<template>
    <div class="mobile-menu-overlay" @click.self="closeSidebar">
        <aside class="mobile-menu mobile-menu--open">
            <button class="menu-close-button" @click="closeSidebar">✕</button>
            <nav class="mobile-nav">
                <ul class="mobile-menu-list">
                    <li class="mobile-menu-item">
                        <a href="" @click.prevent="emit('staffLink')" class="header-menu-link">Мастера</a>
                    </li>
                    <li class="mobile-menu-item">
                        <a href="" @click.prevent="emit('priceLink')" class="header-menu-link">Услуги</a>
                    </li>
                    <li class="header-menu-item">
                        <a href="" @click.prevent="sidebarStore.openCertsSidebar" class="header-menu-link">Сертификаты</a>
                    </li>
                </ul>
            </nav>
            <div class="menu-actions">
                <div class="menu-buttons">
                    <button @click="sidebarStore.openBookingSidebar" class="menu-button menu-appointment-button">
                        Онлайн
                        запись
                    </button>
                    <a href="tel:+79126422020" class="menu-button menu-phone-button">Запись по звонку</a>
                </div>
                <div class="menu-socials">
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
                    <a href="https://vk.com/dabro_sun">
                        <svg width="60" height="60">
                            <use href="#icon-vk"/>
                        </svg>
                    </a>
                </div>
            </div>
        </aside>
    </div>
</template>

<style scoped>
.mobile-menu-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, .55);
    backdrop-filter: blur(4px);
    z-index: 10;
}

.mobile-menu {
    position: fixed;
    top: 0;
    right: 0;
    height: 100%;
    width: 300px;
    background-color: var(--color-light-black);
    color: var(--color-gold);
    padding: 42px 25px;
    transform: translateX(100%);
    transition: transform 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    align-items: center;
    z-index: 4;
}

.mobile-menu--open {
    transform: translateX(0);
}

.menu-close-button {
    position: absolute;
    right: 10px;
    top: 5px;
    background: none;
    border: none;
    font-size: 28px;
    color: var(--color-gold);
}

.mobile-menu-list {
    display: flex;
    flex-direction: column;
    gap: 35px;
    color: var(--color-gold);
    font-size: 24px;
}

.menu-buttons {
    font-size: 18px;
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.menu-button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 200px;
    height: 70px;
}

.menu-appointment-button {
    background-color: var(--color-gold);
    border-radius: 2px;
    color: #000300;
}

.menu-phone-button {
    background-color: transparent;
    border: none;
}

.menu-phone-button:hover {
    border: var(--border);
    border-radius: var(--border-radius);
}

.menu-phone-button:active {
    color: var(--color-gold-hover);
    border: var(--border);
    border-radius: var(--border-radius);
}

.menu-appointment-button:hover {
    background-color: var(--color-gold);
}

.menu-appointment-button:active {
    background-color: var(--color-light-gold);
}
</style>