<script setup>
import PriceItem from "@/components/PriceItem.vue";

const priceList = [
    {
        "id": 1,
        "title": "МУЖСКАЯ СТРИЖКА",
        "price": "1100–1900 ₽",
        "descr": "Стрижка машинкой, ножницами, бритьё шейвером, мытьё головы до/и после стрижки с использованием профессиональных средств.\nПродолжительность 60 мин."
    },
    {
        "id": 2,
        "title": "СТРИЖКА ПОД ОДНУ НАСАДКУ",
        "price": "800–1100 ₽",
        "descr": "Стрижка машинкой, используется max две насадки, мытье головы до/и после стрижки с использованием профессиональных средств.\nПродолжительность 40 мин."
    },
    {
        "id": 3,
        "title": "ОФОРМЛЕНИЕ БОРОДЫ И УСОВ",
        "price": "900–1600 ₽",
        "descr": "Окантовка, стрижка, бритье шейвером, укладка, обработка профессиональными уходовыми средствами.\nПродолжительность 45 мин."
    },
    {
        "id": 4,
        "title": "Камуфляж (закрашивание седины)",
        "price": "от 1100 ₽",
        "descr": "Борода и усы, Голова или Комплекс.\nПродолжительность 45 мин."
    },
    {
        "id": 5,
        "title": "ДВА BRO",
        "price": "2100–2900 ₽",
        "descr": "Оказание двух услуг Мужская стрижка по записи в одно время к одному мастеру"
    },
    {
        "id": 6,
        "title": "МУЖСКАЯ СТРИЖКА +<br>ОФОРМЛЕНИЕ БОРОДЫ",
        "price": "1800–3000 ₽",
        "descr": "Оказание услуг Мужская стрижка и Оформление бороды по записи в одно время к одному мастеру"
    },
    {
        "id": 7,
        "title": "СТРИЖКА ПОД НАСАДКУ +<br>ОФОРМЛЕНИЕ БОРОДЫ",
        "price": "1500–2300 ₽",
        "descr": "Оказание услуг Стрижка под насадку и Оформление бороды по записи в одно время к одному мастеру"
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
            <img src="@/assets/img/logo_short.svg" alt="logo" class="bg-logo"/>
        </div>
    </section>
</template>

<style scoped>
.price {
    margin-top: max(10px, 12vw);
    padding: 0 40px;
}

.price-inner h1 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-weight: 700;
    font-size: clamp(24px, 4.56vw, 60px);
    letter-spacing: 3px;
    text-transform: uppercase;
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