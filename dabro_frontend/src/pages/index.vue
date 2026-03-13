<script setup>
import Banner from "@/components/Banner.vue";
import About from "@/components/About.vue";
import Values from "@/components/Values.vue";
import Staff from "@/components/Staff.vue";
import Gallery from "@/components/Gallery.vue";
import Appointment from "@/components/Appointment.vue";
import Footer from "@/components/Footer.vue";
import {nextTick, onMounted} from "vue";
import {useStaffStore} from "@/stores/staff.js";
import Price from "@/components/Price.vue";
import {getLenis} from "@/plugins/lenis.js";
import {useRoute} from "vue-router";

const staffStore = useStaffStore()
const route = useRoute()

function delay(ms = 250) {
    return new Promise(resolve => setTimeout(resolve, ms))
}

async function scrollFromQuery() {
    const target = route.query.scroll
    if (!target) return

    await nextTick()
    await delay(300)

    const lenis = getLenis()
    if (!lenis) return

    await lenis.scrollTo(`#${target}`, {
        offset: -130
    })
}

onMounted(() => {
    staffStore.loadStaff()
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