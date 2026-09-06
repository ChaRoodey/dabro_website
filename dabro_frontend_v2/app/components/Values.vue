<script setup>

</script>

<template>
    <section class="values">
        <div class="values-inner container">
            <div class="values-logo">
                <img src="@/assets/img/values_logo.svg" alt="logo">
            </div>
            <ul class="values-list">
                <li class="values-item">
                    <p>DA, BRО — МЕСТО, ГДЕ МУЖЧИНЫ ПОЛУЧАЮТ КАЧЕСТВЕННЫЙ СЕРВИС И ПРОФЕССИОНАЛЬНЫЙ УХОД.</p>
                </li>
                <li class="values-item">
                    <p>НАША ФИЛОСОФИЯ- В ГАРМОНИЧНОМ СОЧЕТАНИИ ПРОФЕССИОНАЛИЗМА, ТВОРЧЕСТВА И СВОБОДЫ.</p>
                </li>
                <li class="values-item">
                    <p>СОВОКУПНОСТЬ НАШИХ ПРЕДЛОЖЕНИЙ, СЕРВИСА И КАЧЕСТВА РАБОТЫ ГОВОРИТ САМО ЗА СЕБЯ. ЗДЕСЬ ВАМ
                        РАДЫ.</p>
                </li>
            </ul>
        </div>
    </section>
</template>

<style scoped>
.values {
    width: 100%;
    padding: 100px 32px;
}

.values-inner {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    gap: 40px;
}

.values-logo img {
    opacity: 0.4;
    min-width: 52px;
    min-height: 240px;
}

.values-item {
    margin-top: 20px;
    max-width: 1000px;
}

.values-item p {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-weight: 300;
    font-size: clamp(14px, 2.34vw, 30px);
    letter-spacing: 2px;
}
</style>