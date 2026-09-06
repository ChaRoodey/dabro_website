<script setup lang="ts">
const config = useRuntimeConfig()

useSeoMeta({
    title: 'DaBro — мужской салон в Екатеринбурге',
    description:
        'DaBro — мужской салон в Екатеринбурге. Услуги барбера, онлайн-запись, контакты и информация о салоне.',
    ogTitle: 'DaBro — мужской салон в Екатеринбурге',
    ogDescription:
        'Услуги барбера, онлайн-запись и контакты мужского салона DaBro.',
    ogType: 'website',
    ogLocale: 'ru_RU',
})

useHead({
    link: [
        {
            rel: 'canonical',
            href: `${config.public.siteUrl}/`,
        },
    ],
})
</script>

<template>
    <Banner/>
    <About/>
    <Values/>
    <Staff/>
    <Gallery/>
    <Price/>
    <Appointment/>
    <Footer/>
</template>

<style scoped>

</style>