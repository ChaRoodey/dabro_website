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

function delay(ms = 250) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function scrollFromQuery() {
    const route = useRoute()
    const target = route.query.scroll
    if (!target) return

    await nextTick()
    await delay(300)

    const lenis = getLenis()
    if (!lenis) return

    await lenis.scrollTo(`#${target}`, {
        offset: -200
    })
}

onMounted(() => {
    scrollFromQuery()
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