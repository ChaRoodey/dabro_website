<script setup>

import Carusel from "@/components/Carusel.vue";
</script>

<template>
    <section class="about" id="about">
        <div class="about-inner container">
            <h1>у нас</h1>
            <div class="about-content">
                <div class="about-carousel">
                    <span class="line top"></span>
                    <span class="line bottom"></span>
                    <div class="about-carousel-inner">
                        <Carusel>
                            <div class="slide">
                                <img src="@/assets/img/about_7.jpg" alt="">
                            </div>
                            <div class="slide">
                                <img src="@/assets/img/about_5.jpg" alt="">
                            </div>
                            <div class="slide">
                                <img src="@/assets/img/about_6.jpg" alt="">
                            </div>
                            <div class="slide">
                                <img src="@/assets/img/about_8.jpg" alt="">
                            </div>
                        </Carusel>
                    </div>
                </div>
                <div class="about-qualities">
                    <ul class="about-qualities-list">
                        <li class="about-qualities-item">
                            <div class="about-qualities-title">
                                <h2>сервис</h2>
                            </div>
                            <div class="about-qualities-description">
                                <p>Мы не боимся вопросов: «а как лучше?», «а может, длиннее?» или «давай что‑то
                                    новое?».
                                    Мы
                                    даём
                                    ответы на эти вопросы.</p>
                            </div>
                        </li>
                        <li class="about-qualities-item">
                            <div class="about-qualities-title">
                                <h2>качество</h2>
                            </div>
                            <div class="about-qualities-description">
                                <p>Не станем говорить, что мы лучшие. Нет, мы только стремимся к этому. Но одно
                                    можем
                                    сказать
                                    точно: «Качество будет видно издалека»!</p>
                            </div>
                        </li>
                        <li class="about-qualities-item">
                            <div class="about-qualities-title">
                                <h2>атмосфера</h2>
                            </div>
                            <div class="about-qualities-description">
                                <p>Интересная. У нас можно не только подстричься. Ещё мы играем в настольные игры со
                                    своими
                                    гостями в назначенное время (подробности в телеграм-канале).</p>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.slide {
    height: 600px;
}

.slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.about {
    min-height: 800px;
    width: 100%;
    padding: 100px 32px;
}

.about-inner {
    display: flex;
    justify-content: center;
    flex-direction: column;
    align-items: center;
}

.about-inner h1 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-size: clamp(36px, 4.28vw, 60px);
    font-weight: 700;
    letter-spacing: 3px;
    margin: 10px auto;
}

.about-content {
    margin: 0 auto;
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 80px;
    width: 100%;
}

.about-carousel {
    position: relative;
    width: clamp(300px, 26vw, 440px);
    height: auto;
}

.about-carousel-inner {
    position: relative;
    overflow: hidden;
    z-index: 2;
}

.about-carousel-inner img {
    filter: grayscale(100%);
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.about-carousel::before,
.about-carousel::after {
    content: "";
    position: absolute;
    top: 5%;
    bottom: 35%;
    width: 1px;
    background-color: var(--color-gold);
}

.about-carousel::before {
    left: -20px;
}

.about-carousel::after {
    right: -20px;
}

.line {
    position: absolute;
    left: -20px;
    right: -20px;
    height: 1px;
    background: var(--color-gold);
}

.about-carousel .line.top {
    top: 5%;
    z-index: 3;
}

.about-carousel .line.bottom {
    bottom: 35%;
    z-index: 1;
}

.about-carousel-track {
    display: flex;
    transition: transform 0.5s ease-in-out;
}

.about-carousel-track img {
    object-fit: cover;
    flex-shrink: 0;
}

.about-carousel button {
    position: absolute;
    top: 50%;
    width: 30px;
    height: 30px;
    transform: translateY(-50%);
    background: #cdcdcd;
    color: #131512;
    border: none;
    /*padding: 10px 15px;*/
    cursor: pointer;
    border-radius: 50%;
}

.about-carousel button:hover {
    color: #b5b5b5;
}

.about-carousel-prev {
    left: 10px;
}

.about-carousel-next {
    right: 10px;
}

.about-qualities-list {
    display: flex;
    flex-direction: column;
}

.about-qualities-item {
    display: flex;
    flex-direction: row;
    margin-top: 40px;
}

.about-qualities-title {
    width: 200px;
}

.about-qualities-description {
    width: 460px;
}

.about-qualities-title h2 {
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: clamp(16px, 2.3vw, 24px);
    font-weight: 400;
    text-transform: uppercase;
    margin: 0;
}

.about-qualities-description p {
    font-family: var(--font-family-base), Arial, sans-serif;
    font-size: clamp(16px, 2.3vw, 24px);
    font-weight: 400;
}

@media (max-width: 1280px) {
    .about {
        padding: 50px 16px;
    }

    .about-content {
        flex-direction: column;
        align-items: center;
    }

    .about-carousel {
        order: 1;
    }

    .about {
        padding: 70px 32px;
    }
}

@media (max-width: 680px) {
    .about {
        padding: 30px 18px;
    }

    .about-qualities-item {
        flex-direction: column;
    }

    .about-qualities-title {
        margin-bottom: 10px;
    }

    .about-qualities-description {
        width: 300px;
    }

}
</style>