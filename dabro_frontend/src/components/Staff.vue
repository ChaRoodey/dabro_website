<script setup>
import StaffCard from "@/components/StaffCard.vue";
import {useStaffStore} from "@/stores/staff.js";

const staffStore = useStaffStore()
</script>

<template>
    <section class="staff" id="staff">
        <div class="staff-inner container">
            <h1>наши мастера</h1>
            <div class="staff-carousel-wrapper">
                <button class="staff-carousel-btn prev">&#10094;</button>
                <button class="staff-carousel-btn next">&#10095;</button>
                <ul class="staff-list">
                    <li class="staff-item"
                        v-for="staff in staffStore.allStaff"
                        :key="staffStore.allStaff?.staff_id"
                    >
                        <StaffCard :staffInfo="staff"/>
                    </li>
                </ul>
            </div>
        </div>
    </section>
</template>

<style scoped>
.staff-inner {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: clamp(32px, 7.69vw, 100px);
}

.staff-inner h1 {
    font-family: var(--font-family-accent), Arial, sans-serif;
    font-weight: 700;
    font-size: clamp(24px, 4.56vw, 60px);
    letter-spacing: 3px;
    text-transform: uppercase;
}

.staff-carousel-wrapper {
    position: relative;
    overflow: hidden;
}

.staff-carousel-btn {
    position: absolute;
    top: 40%;
    z-index: 3;
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

.staff-carousel-btn:hover {
    color: #b5b5b5;
}

.staff-carousel-btn.next {
    right: 10px;
}

.staff-carousel-btn.prev {
    display: none;
    left: 10px;
}

.staff-list {
    display: flex;
    flex-direction: row;
    gap: 0;
    transition: transform 0.5s ease-in-out;
}

.staff-item {
    flex: 0 0 clamp(200px, 25vw, 300px);
    margin-right: 50px;
    justify-content: center;
}
</style>