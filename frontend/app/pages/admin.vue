<script setup>
import {useStaffStore} from "../stores/staff.js";
import {usePhotosStore} from "../stores/photos.js";
import {startLenis, stopLenis} from "../utils/lenis.js";

const staffStore = useStaffStore()
const photosStore = usePhotosStore()

const isModalOpen = ref(false);
const selectedPhoto = ref(null);
const objectId = ref(null);
const instance = ref(null);

function handleSelect(object, inst) {
    selectedPhoto.value = object.img_url
    objectId.value = object.product_id || object.staff_id
    instance.value = inst
    isModalOpen.value = true;

    stopLenis()
    document.body.style.overflow = "hidden"
}

function handleClose() {
    isModalOpen.value = false;
    selectedPhoto.value = null
    objectId.value = null
    instance.value = null

    startLenis()
    document.body.style.overflow = ""
}

function handleApply(payload) {
    if (payload.instance === 'staff') {
        const staff = staffStore.allStaff.find(staff => staff.staff_id === payload.id)
        if (staff) {
            staff.img_url = payload.img_url
        }
        photosStore.addNewPhoto(payload)
    }
}

function addStaffRow() {
    staffStore.allStaff.push({
        staff_id: Date.now(),
        name: "",
        grade: "",
        description: "",
        img_url: null,
    })
}

function deleteStaffMember(staffId) {
    staffStore.deleteStaff(staffId)
}

onMounted(() => {
    staffStore.loadStaff()
})
</script>

<template>
    <main class="admin container">
        <header class="admin-header">
            <h1 class="admin-header-title">Админ-панель</h1>
            <!--            <p class="admin-header-subtitle">Картинки, сотрудники, импорт товаров из Excel</p>-->
        </header>

        <!-- Staff -->
        <section class="admin-card">
            <div class="card__head staff-head">
                <h2>Сотрудники</h2>

                <div class="staff-actions">
                    <button
                            class="base-black-btn btn"
                            @click="staffStore.uploadStaff"
                            :disabled="staffStore.uploadingStaff"
                    >
                        {{ staffStore.uploadingStaff ? "..." : "Сохранить" }}
                    </button>

                    <button
                            class="btn base-black-btn"
                            @click="staffStore.loadStaff"
                            :disabled="staffStore.loadingStaff"
                    >
                        {{ staffStore.loadingStaff ? "Загрузка..." : "Обновить" }}
                    </button>

                    <button class="btn base-black-btn" @click="addStaffRow">+ Добавить сотрудника</button>
                </div>
            </div>

            <!--            <p v-if="staffError" class="error">{{ staffError }}</p>-->

            <div class="table">
                <div class="table-row table-row-staff table-row-head">
                    <div>Имя</div>
                    <div>Должность</div>
                    <div>Описание</div>
                    <div>Фото</div>
                    <div></div>
                </div>
                <div class="table-content" data-lenis-prevent-wheel>
                    <div class="table-row table-row-staff" v-for="m in staffStore.allStaff" :key="m.staff_id">
                        <div>
                            <input class="input" v-model="m.name" placeholder="Имя"/>
                        </div>
                        <div>
                            <input class="input" v-model="m.grade" placeholder="Должность"/>
                        </div>
                        <div>
                            <input class="input" v-model="m.description" placeholder="Описание"/>
                        </div>
                        <div>
                            <div class="photo-cell" @click="handleSelect(m, 'staff')">
                                <img v-if="m.img_url" :src="m.img_url" alt="Staff photo" class="photo-thumb btn"/>
                                <button v-else class="btn-placeholder btn">—</button>
                            </div>
                        </div>

                        <div class="row-actions">
                            <button class="btn base-black-btn" @click="deleteStaffMember(m.staff_id)">
                                {{ staffStore.staffDeleting ? "Удаление.." : "Удалить" }}
                            </button>
                        </div>

                        <div v-if="m.error" class="error table__error">{{ m.error }}</div>
                    </div>
                </div>
            </div>
        </section>

        <PhotoModal
                v-if="isModalOpen"
                :currPhotoUrl="selectedPhoto"
                :objectId="objectId"
                :instance="instance"
                @apply="handleApply"
                @close="handleClose"
        />
        <StatusModal
                v-if="staffStore.adminError || staffStore.adminSuccess"
                :errorMessage="staffStore.adminError"
                :successMessage="staffStore.adminSuccess"
        />
    </main>
</template>

<style scoped>

.excel-result__head h3 {
    margin: 0;
    font-size: 22px;
}

.admin {
    padding: 24px 16px 60px;
}

.admin h2 {
    font-size: 36px;
}

.admin-header {
    margin: 0 0 18px 30px;
}

.admin-header-title {
    font-size: 46px;
    margin: 0 0 6px;
}

.admin-card {
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 12px;
    padding: 16px;
    margin-top: 16px;
    background: rgba(255, 255, 255, 0.02);
}

.card__head {
    margin-bottom: 12px;
}

.image-item__preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.base-black-btn {
    padding: 8px 18px;
    /*border-radius: 2px;*/
    cursor: pointer;
    background: transparent;
    border: 1px solid var(--color-gold);
}

.btn:hover {
    border: var(--border-hover);
    transform: scale(1.01) translateY(-5%);
}

.btn:active {
    transform: translateY(1%)
}

.btn:disabled {
    opacity: 0.6;
    cursor: default;
}

.photo-cell {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.photo-thumb {
    width: 44px;
    height: 44px;
    object-fit: cover;
    border-radius: 8px;
    border: 1px solid #2b2b2b;
    cursor: pointer;
    transition: 0.3s ease;
}

.btn-placeholder {
    width: 44px;
    height: 44px;
    border: 1px dashed #444;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: transparent;
}

.input {
    width: 100%;
    height: 36px;
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: transparent;
    padding: 0 10px;
    color: inherit;
}

.staff-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.staff-actions {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.table {
    display: grid;
    gap: 8px;
}

.table-row {
    display: grid;
    gap: 8px;
    align-items: center;
}

.table-content {
    max-height: 500px;
    overflow-y: auto;
    overscroll-behavior: contain;
}

.table-row-head {
    opacity: 0.7;
    font-size: 13px;
}

.table-row-staff {
    grid-template-columns: 1fr 1fr 1.6fr 0.15fr 110px;
}

@media (max-width: 980px) {
    .table-row {
        grid-template-columns: 1fr;
    }

    .table-row-head {
        display: none;
    }
}

.row-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
}

.table__error {
    grid-column: 1 / -1;
}

.error {
    color: #ff6b6b;
    margin: 0;
}

.result pre {
    background: rgba(0, 0, 0, 0.3);
    padding: 10px;
    border-radius: 10px;
    overflow: auto;
}
</style>