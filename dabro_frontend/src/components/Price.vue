<script setup>
import PriceItem from "@/components/PriceItem.vue";

const priceList = [
    {
        "id": 1,
        "title": "МУЖСКАЯ СТРИЖКА",
        "price": "1200–1500 ₽",
        "descr": "Стрижка машинкой, ножницами, бритьё шейвером, мытьё головы до/и после стрижки с использованием профессиональных средств.\nПродолжительность 60 мин."
    },
    {
        "id": 2,
        "title": "СТРИЖКА ПОД ОДНУ НАСАДКУ",
        "price": "720–900 ₽",
        "descr": "Стрижка машинкой, используется max две насадки, мытье головы до/и после стрижки с использованием профессиональных средств.\nПродолжительность 40 мин."
    },
    {
        "id": 3,
        "title": "КОРРЕКЦИЯ БОРОДЫ И УСОВ",
        "price": "800–1200 ₽",
        "descr": "Окантовка, стрижка, бритье шейвером, укладка, обработка профессиональными уходовыми средствами.\nПродолжительность 45 мин."
    },
    {
        "id": 4,
        "title": "КОРРЕКЦИЯ БОРОДЫ И УСОВ",
        "price": "800–1200 ₽",
        "descr": "Окантовка, стрижка, бритье шейвером, укладка, обработка профессиональными уходовыми средствами.\nПродолжительность 45 мин."
    },
    {
        "id": 5,
        "title": "Камуфляж (закрашивание седины)",
        "price": "от 1000 ₽",
        "descr": "Борода и усы, Голова или Комплекс.\nПродолжительность 45 мин."
    },
]
</script>

<template>
    <section class="price" id="price">
        <div class="price-inner container">
            <h1>услуги</h1>
            <div class="price-list">
                <PriceItem
                        v-for="item of priceList"
                        :key="item.id"
                        :item="item"
                        class="price-item"
                />
            </div>
            <img src="@/assets/img/logo_short.svg" alt="logo" class="bg-logo" />
        </div>
    </section>
</template>

<style scoped>
.price {
    margin-top: max(10px, 12vw);
}

.price-list {
    column-count: 2;
    column-gap: 40px;
}

.price-item {
    break-inside: avoid;
    margin-bottom: 20px;
}

@media (max-width: 768px) {
    .price-list {
        column-count: 1;
    }
}

.bg-logo {
    width: 100%;
    opacity: 0.1;
}
</style>