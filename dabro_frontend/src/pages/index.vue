<script setup>
import Banner from "@/components/Banner.vue";
import About from "@/components/About.vue";
import Values from "@/components/Values.vue";
import Staff from "@/components/Staff.vue";
import Gallery from "@/components/Gallery.vue";
import Appointment from "@/components/Appointment.vue";
import Footer from "@/components/Footer.vue";
import {onMounted} from "vue";
import {useStaffStore} from "@/stores/staff.js";
import Price from "@/components/Price.vue";

const staffStore = useStaffStore()

onMounted(() => {
    staffStore.loadStaff()
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