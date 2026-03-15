<script setup>
import {computed, onMounted, ref} from "vue";
import {useStaffStore} from "@/stores/staff.js";
import {usePhotosStore} from "@/stores/photos.js";
import {useProductsStore} from "@/stores/products.js";
import PhotoModal from "@/components/PhotoModal.vue";
import {startLenis, stopLenis} from "@/plugins/lenis.js";
import StatusModal from "@/components/StatusModal.vue";

const staffStore = useStaffStore()
const productStore = useProductsStore()
const photosStore = usePhotosStore()

const isModalOpen = ref(false);
const selectedPhoto = ref(null);
const objectId = ref(null);
const instance = ref(null);
const isExcelDetailsOpen = ref(false)

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
    if (payload.instance === 'product') {
        const product = productStore.allProducts.find(product => product.product_id === payload.id)
        if (product) {
            product.img_url = payload.img_url
        }
        photosStore.addNewPhoto(payload)
    } else if (payload.instance === 'staff') {
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

function addProductRow() {
    productStore.allProducts.push({
        product_id: Date.now(),
        brand: "",
        description: "",
        size: "",
        category: "",
        img_url: "",
        excel_product_id: null,
        cost: null,
        items_left: null,
    })
}

function deleteStaffMember(staffId) {
    staffStore.deleteStaff(staffId)
}

function onPickExcel(file) {
    productStore.excelError = '';

    if (!file) {
        productStore.excelFile = null;
        return;
    }

    const okExt = file.name.toLowerCase().endsWith(".xlsx");
    if (!okExt) {
        productStore.excelError = 'Нужен файл .xlsx';
        return;
    }
    productStore.excelFile = file
}

function uploadExcel() {
    isExcelDetailsOpen.value = false
    productStore.uploadProductsExcel()
}

const excelSummary = computed(() => {
    return productStore.excelResults || null
})

const excelDetails = computed(() => {
    return excelSummary.value?.details || []
})

const excelValidationErrors = computed(() => {
    return excelSummary.value?.errors || []
})

const isExcelSuccess = computed(() => {
    return excelSummary.value?.status === 'ok'
})

const isExcelValidationError = computed(() => {
    return excelSummary.value?.status === 'validation_error'
})

const hasExcelResultObject = computed(() => {
    return !!excelSummary.value && typeof excelSummary.value === 'object'
})

function actionLabel(action) {
    switch (action) {
        case 'added':
            return 'Добавлен'
        case 'updated':
            return 'Обновлён'
        case 'no_changes':
            return 'Без изменений'
        default:
            return action
    }
}

function actionClass(action) {
    switch (action) {
        case 'added':
            return 'status-added'
        case 'updated':
            return 'status-updated'
        case 'no_changes':
            return 'status-skipped'
        default:
            return ''
    }
}

function excelStatusLabel(status) {
    switch (status) {
        case 'ok':
            return 'Успешно'
        case 'validation_error':
            return 'Ошибка валидации'
        default:
            return 'Результат'
    }
}

function excelStatusClass(status) {
    switch (status) {
        case 'ok':
            return 'excel-result__badge--ok'
        case 'validation_error':
            return 'excel-result__badge--error'
        default:
            return ''
    }
}

const fieldLabels = {
    brand: 'Брэнд',
    category: 'Категория',
    title: 'Название',
    description: 'Описание',
    size: 'Объем',
    cost: 'Стоимость',
    items_left: 'Остаток',
    excel_product_id: 'ID',
    id: 'ID',
}

function toggleExcelDetails() {
    isExcelDetailsOpen.value = !isExcelDetailsOpen.value
}

onMounted(() => {
    staffStore.loadStaff()
    productStore.loadProducts()
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

        <!-- Products -->
        <section class="admin-card">
            <div class="card__head staff-head">
                <h2>Товары</h2>

                <div class="staff-actions">
                    <button
                            class="btn base-black-btn"
                            @click="productStore.uploadProducts"
                            :disabled="productStore.productsUploading"
                    >
                        {{ productStore.productsUploading ? "Сохранение.." : "Сохранить" }}
                    </button>

                    <button
                            class="btn base-black-btn"
                            @click="productStore.loadProducts"
                            :disabled="productStore.productsLoading"
                    >
                        {{ productStore.productsLoading ? "Загрузка..." : "Обновить" }}
                    </button>

                    <button class="base-black-btn btn" @click="addProductRow">+ Добавить товар</button>
                </div>
            </div>

            <!--            <p v-if="staffError" class="error">{{ staffError }}</p>-->

            <div class="table">
                <div class="table-row table-row-product table-row-head">
                    <div>ID</div>
                    <div>Брэнд</div>
                    <div>Категория</div>
                    <div>Название</div>
                    <div>Описание</div>
                    <div>Объем</div>
                    <div>Цена</div>
                    <div>Остаток</div>
                    <div>Фото</div>
                    <div></div>
                </div>
                <div class="table-content" data-lenis-prevent-wheel>
                    <div class="table-row table-row-product" v-for="p in productStore.allProducts" :key="p.product_id">
                        <div>
                            <input class="input" v-model="p.excel_product_id" placeholder="ID"/>
                        </div>
                        <div>
                            <input class="input" v-model="p.brand" placeholder="Брэнд"/>
                        </div>
                        <div>
                            <input class="input" v-model="p.category" placeholder="Категория"/>
                        </div>
                        <div>
                            <input class="input" v-model="p.title" placeholder="Название"/>
                        </div>
                        <div>
                            <input class="input" v-model="p.description" placeholder="Описание"/>
                        </div>
                        <div>
                            <input class="input" v-model="p.size" placeholder="Объем"/>
                        </div>
                        <div>
                            <input class="input" v-model="p.cost" placeholder="Цена"/>
                        </div>
                        <div>
                            <input class="input" v-model="p.items_left" placeholder="Остаток"/>
                        </div>
                        <div>
                            <div class="photo-cell" @click="handleSelect(p, 'product')">
                                <img v-if="p.img_url" :src="p.img_url" alt="Product photo" class="photo-thumb btn"/>
                                <button v-else class="btn-placeholder btn">—</button>
                            </div>
                        </div>
                        <div class="row-actions">
                            <button class="base-black-btn btn" @click="productStore.deleteProduct(p.product_id)">
                                {{ productStore.productsDeleting ? "Удаление.." : "Удалить" }}
                            </button>
                        </div>
                    </div>

                    <!--                    <div v-if="m.error" class="error table__error">{{ m.error }}</div>-->
                </div>
            </div>
        </section>

        <!-- Excel -->
        <section class="admin-card">
            <div class="excel-inner">
                <div class="excel-actions">
                    <div class="card__head">
                        <h2>Импорт товаров из Excel</h2>
                        <p class="muted">Загрузите файл .xlsx/.xls с актуальными ценами и остатками</p>
                    </div>

                    <div class="excel">
                        <input
                                type="file"
                                accept=".xlsx,.xls,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.ms-excel"
                                @change="onPickExcel($event.target.files?.[0] || null)"
                        />

                        <button class="base-black-btn btn" :disabled="productStore.excelUploading" @click="uploadExcel">
                            {{ productStore.excelUploading ? "Загрузка..." : "Загрузить и обновить" }}
                        </button>
                    </div>
                </div>

                <div v-if="hasExcelResultObject" class="excel-result">
                    <div class="excel-result__head">
                        <h3>Результат импорта</h3>
                        <span
                                class="excel-result__badge"
                                :class="excelStatusClass(excelSummary.status)"
                        >
                            {{ excelStatusLabel(excelSummary.status) }}
                        </span>
                    </div>

                    <p v-if="excelSummary.message" class="excel-result__message">
                        {{ excelSummary.message }}
                    </p>

                    <template v-if="isExcelSuccess">
                        <div class="excel-stats">
                            <div class="excel-stat excel-stat--added">
                                <span class="excel-stat__label">Добавлено</span>
                                <strong class="excel-stat__value">{{ excelSummary.added ?? 0 }}</strong>
                            </div>

                            <div class="excel-stat excel-stat--updated">
                                <span class="excel-stat__label">Обновлено</span>
                                <strong class="excel-stat__value">{{ excelSummary.updated ?? 0 }}</strong>
                            </div>

                            <div class="excel-stat excel-stat--skipped">
                                <span class="excel-stat__label">Без изменений</span>
                                <strong class="excel-stat__value">{{ excelSummary.skipped ?? 0 }}</strong>
                            </div>
                        </div>

                        <div v-if="excelDetails.length" class="excel-details-toggle">
                            <button class="base-black-btn btn" @click="toggleExcelDetails">
                                {{ isExcelDetailsOpen ? 'Скрыть детали' : `Показать детали (${excelDetails.length})` }}
                            </button>
                        </div>

                        <div v-if="excelDetails.length && isExcelDetailsOpen" class="excel-log">
                            <div class="excel-log__head">
                                <div>Строка</div>
                                <div>ID товара</div>
                                <div>Статус</div>
                                <div>Изменения</div>
                            </div>

                            <div
                                    v-for="item in excelDetails"
                                    :key="`${item.row}-${item.excel_id}-${item.action}`"
                                    class="excel-log__row"
                            >
                                <div class="excel-log__cell">
                                    {{ item.row }}
                                </div>

                                <div class="excel-log__cell">
                                    {{ item.excel_id }}
                                </div>

                                <div class="excel-log__cell">
                                    <span class="status-pill" :class="actionClass(item.action)">
                                        {{ actionLabel(item.action) }}
                                    </span>
                                </div>

                                <div class="excel-log__cell">
                                    <template v-if="item.fields?.length">
                                        <span
                                                v-for="field in item.fields"
                                                :key="field"
                                                class="field-badge"
                                        >
                                            {{ fieldLabels[field] || field }}
                                        </span>
                                    </template>
                                    <span v-else class="muted">—</span>
                                </div>
                            </div>
                        </div>
                    </template>

                    <template v-else-if="isExcelValidationError">
                        <div class="excel-stats excel-stats--single">
                            <div class="excel-stat excel-stat--error">
                                <span class="excel-stat__label">Ошибок найдено</span>
                                <strong class="excel-stat__value">{{ excelValidationErrors.length }}</strong>
                            </div>
                        </div>

                        <div v-if="excelValidationErrors.length" class="excel-details-toggle">
                            <button class="base-black-btn btn" @click="toggleExcelDetails">
                                {{
                                    isExcelDetailsOpen ? 'Скрыть ошибки' : `Показать ошибки (${excelValidationErrors.length})`
                                }}
                            </button>
                        </div>

                        <div v-if="excelValidationErrors.length && isExcelDetailsOpen" class="excel-log">
                            <div class="excel-log__head excel-log__head--errors">
                                <div>Строка</div>
                                <div>Поле</div>
                                <div>Ошибка</div>
                            </div>

                            <div
                                    v-for="(item, idx) in excelValidationErrors"
                                    :key="`${item.row}-${item.field}-${idx}`"
                                    class="excel-log__row excel-log__row--errors"
                            >
                                <div class="excel-log__cell">
                                    {{ item.row }}
                                </div>

                                <div class="excel-log__cell">
                                    {{ fieldLabels[item.field] || item.field || '—' }}
                                </div>

                                <div class="excel-log__cell excel-log__cell--error-text">
                                    {{ item.message }}
                                </div>
                            </div>
                        </div>
                    </template>
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
                v-if="productStore.adminError || productStore.adminSuccess"
                :errorMessage="productStore.adminError"
                :successMessage="productStore.adminSuccess"
        />
    </main>
</template>

<style scoped>
.excel-result__message {
    margin: 0;
    opacity: 0.85;
}

.excel-result__badge--error {
    color: #ff8e8e;
    border-color: rgba(255, 107, 107, 0.35);
    background: rgba(255, 107, 107, 0.1);
}

.excel-stats--single {
    grid-template-columns: minmax(0, 220px);
}

.excel-stat--error {
    border-color: rgba(255, 107, 107, 0.22);
}

.excel-log__head--errors,
.excel-log__row--errors {
    grid-template-columns: 90px 180px 1fr;
}

.excel-log__cell--error-text {
    color: #ffb0b0;
}

.excel-details-toggle {
    display: flex;
    justify-content: flex-start;
}

.excel-inner {
    display: flex;
    flex-direction: row;
    align-items: start;
    justify-content: space-around;
}

.excel-result {
    margin-top: 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    padding: 14px;
    background: rgba(255, 255, 255, 0.03);
    display: grid;
    gap: 14px;
}

.excel-result__head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
}

.excel-result__head h3 {
    margin: 0;
    font-size: 22px;
}

.excel-result__badge {
    display: inline-flex;
    align-items: center;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 13px;
    border: 1px solid rgba(255, 255, 255, 0.12);
    background: rgba(255, 255, 255, 0.04);
}

.excel-result__badge--ok {
    color: #7ee787;
    border-color: rgba(126, 231, 135, 0.35);
    background: rgba(126, 231, 135, 0.08);
}

.excel-stats {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 10px;
}

.excel-stat {
    border-radius: 12px;
    padding: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    background: rgba(0, 0, 0, 0.18);
    display: grid;
    gap: 6px;
}

.excel-stat__label {
    font-size: 13px;
    opacity: 0.75;
}

.excel-stat__value {
    font-size: 28px;
    line-height: 1;
}

.excel-stat--added {
    border-color: rgba(126, 231, 135, 0.22);
}

.excel-stat--updated {
    border-color: rgba(255, 196, 87, 0.22);
}

.excel-stat--skipped {
    border-color: rgba(160, 160, 160, 0.2);
}

.excel-log {
    display: grid;
    gap: 8px;
}

.excel-log__head,
.excel-log__row {
    display: grid;
    grid-template-columns: 90px 1fr 160px 1.5fr;
    gap: 10px;
    align-items: start;
}

.excel-log__head {
    font-size: 13px;
    opacity: 0.65;
    padding: 0 4px;
}

.excel-log__row {
    padding: 12px;
    border-radius: 12px;
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.06);
}

.excel-log__cell {
    min-width: 0;
    word-break: break-word;
}

.status-pill {
    display: inline-flex;
    align-items: center;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 13px;
    line-height: 1;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.status-added {
    color: #7ee787;
    border-color: rgba(126, 231, 135, 0.35);
    background: rgba(126, 231, 135, 0.08);
}

.status-updated {
    color: #ffcc66;
    border-color: rgba(255, 204, 102, 0.35);
    background: rgba(255, 204, 102, 0.08);
}

.status-skipped {
    color: #c9c9c9;
    border-color: rgba(201, 201, 201, 0.2);
    background: rgba(201, 201, 201, 0.06);
}

.field-badge {
    display: inline-flex;
    align-items: center;
    margin: 0 6px 6px 0;
    padding: 5px 9px;
    border-radius: 999px;
    font-size: 12px;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
}

@media (max-width: 980px) {
    .excel-stats {
        grid-template-columns: 1fr;
    }

    .excel-log__head {
        display: none;
    }

    .excel-log__row {
        grid-template-columns: 1fr;
    }
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

.admin-header-subtitle {
    margin: 0;
    opacity: 0.75;
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

.muted {
    opacity: 0.7;
    margin: 6px 0 0;
}

.image-item__preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.base-black-btn {
    padding: 8px 18px;
    //border-radius: 2px;
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

.table-row-product {
    padding-right: 15px;
    grid-template-columns: 0.35fr 0.7fr 1fr 2fr 2fr 0.5fr 0.5fr 0.25fr 0.25fr 110px;
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

.excel-actions {
    display: grid;
    gap: 10px;
    max-width: 600px;
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