<script setup>
import Header from "@/components/Header.vue";
import Banner from "@/components/Banner.vue";
import About from "@/components/About.vue";
import Values from "@/components/Values.vue";
import Staff from "@/components/Staff.vue";
import Gallery from "@/components/Gallery.vue";
import Appointment from "@/components/Appointment.vue";
import Footer from "@/components/Footer.vue";
import {onMounted} from "vue";
import {useStaffStore} from "@/stores/staff.js";

const staffStore = useStaffStore()

onMounted(() => {
    staffStore.loadStaff()
})
</script>

<template>
    <Header/>
    <Banner/>
    <About/>
    <Values/>
    <Staff/>
    <Gallery/>
    <Appointment/>
    <Footer/>
</template>

<style scoped>

</style>