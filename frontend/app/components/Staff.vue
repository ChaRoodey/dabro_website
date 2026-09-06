<script setup>
const config = useRuntimeConfig()

const {data: staff, error} = await useAsyncData(
    'staff',
    () =>
        $fetch('/staff/all', {
            baseURL: config.public.apiBase,
        }),
    {
        default: () => [],
    },
)
</script>

<template>
    <section class="staff" id="staff">
        <div class="staff-inner container">
            <div class="staff-content-wrapper">
                <h1>наши мастера</h1>
                <div class="staff-list">
                    <StaffCard
                            v-for="person in staff"
                            :key="person.staff_id"
                            :staffInfo="person"
                    />
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.staff-inner {
    padding: 0 40px;
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

.staff-list {
    display: grid;
    gap: 50px;
    align-items: center;
    grid-template-columns: 1fr 1fr 1fr;
}

@media (max-width: 1000px) {
    .staff-list {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 680px) {
    .staff-list {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
}
</style>