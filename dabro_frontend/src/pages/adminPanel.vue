<script setup>
import {useStaffStore} from "@/stores/staff.js";
import {onMounted} from "vue";
import {useProductsStore} from "@/stores/products.js";
import Header from "@/components/Header.vue";

const staffStore = useStaffStore()
const productStore = useProductsStore()

function addStaffRow() {
    staffStore.allStaff.push({
        staff_id: `temp_${Date.now()}`,
        name: "",
        grade: "",
        description: "",
        img_id: null,
    })
}

function addProductRow() {
    productStore.allProducts.push({
        product_id: `temp_${Date.now()}`,
        brand: "",
        description: "",
        size: "",
        category: "",
        img_id: "",
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
    productStore.uploadProductsExcel()
}

onMounted(() => {
    staffStore.loadStaff()
    productStore.loadProducts()
})
</script>

<template>
    <Header/>
    <main class="admin container">
        <header class="admin-header">
            <h1 class="admin-header-title">Админ-панель</h1>
            <p class="admin-header-subtitle">Картинки, сотрудники, импорт товаров из Excel</p>
        </header>

        <!-- Images -->
        <!--        <section class="admin-card">-->
        <!--            <div class="card__head">-->
        <!--                <h2>Картинки сайта (8 шт.)</h2>-->
        <!--                <p class="muted">Выберите файл → проверьте превью → нажмите “Сохранить”</p>-->
        <!--            </div>-->

        <!--            <div class="images-grid">-->
        <!--                <div class="image-item" v-for="(img, idx) in images" :key="img.key">-->
        <!--                    <div class="image-item__top">-->
        <!--                        <div class="badge">{{ img.key }}</div>-->
        <!--                    </div>-->

        <!--                    <div class="image-item__preview">-->
        <!--                        <img v-if="img.previewUrl" :src="img.previewUrl" alt=""/>-->
        <!--                        <img v-else-if="img.currentUrl" :src="img.currentUrl" alt=""/>-->
        <!--                        <div v-else class="placeholder">Нет картинки</div>-->
        <!--                    </div>-->

        <!--                    <div class="image-item__controls">-->
        <!--                        <input-->
        <!--                                type="file"-->
        <!--                                accept="image/*"-->
        <!--                                @change="onPickImageFile(idx, $event.target.files?.[0] || null)"-->
        <!--                        />-->

        <!--                        <button class="btn" :disabled="img.saving" @click="saveImage(idx)">-->
        <!--                            {{ img.saving ? "Сохранение..." : "Сохранить" }}-->
        <!--                        </button>-->

        <!--                        <p v-if="img.error" class="error">{{ img.error }}</p>-->
        <!--                    </div>-->
        <!--                </div>-->
        <!--            </div>-->
        <!--        </section>-->

        <!-- Staff -->
        <section class="admin-card">
            <div class="card__head staff-head">
                <h2>Сотрудники</h2>

                <div class="staff-actions">
                    <button
                            class="btn"
                            @click="staffStore.uploadStaff"
                            :disabled="staffStore.uploadingStaff"
                    >
                        {{ staffStore.uploadingStaff ? "..." : "Сохранить" }}
                    </button>

                    <button
                            class="btn btn--secondary"
                            @click="staffStore.loadStaff"
                            :disabled="staffStore.loadingStaff"
                    >
                        {{ staffStore.loadingStaff ? "Загрузка..." : "Обновить" }}
                    </button>

                    <button class="btn" @click="addStaffRow">+ Добавить сотрудника</button>
                </div>
            </div>

            <!--            <p v-if="staffError" class="error">{{ staffError }}</p>-->

            <div class="table">
                <div class="table-row table-row-staff table-row-head">
                    <div>Имя</div>
                    <div>Должность</div>
                    <div>Описание</div>
                    <div>Фото (url)</div>
                    <div></div>
                </div>

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
                        <input class="input" v-model="m.img_id" placeholder="-1"/>
                    </div>

                    <div class="row-actions">
                        <button class="btn" @click="deleteStaffMember(m.staff_id)">Удалить</button>
                    </div>

                    <div v-if="m.error" class="error table__error">{{ m.error }}</div>
                </div>
            </div>
        </section>

        <!-- Products -->
        <section class="admin-card">
            <div class="card__head staff-head">
                <h2>Товары</h2>

                <div class="staff-actions">
                    <button
                            class="btn"
                            @click="productStore.uploadProducts"
                            :disabled="productStore.productsUploading"
                    >
                        {{ staffStore.uploadingStaff ? "..." : "Сохранить" }}
                    </button>

                    <button
                            class="btn btn--secondary"
                            @click="productStore.loadProducts"
                            :disabled="productStore.productsLoading"
                    >
                        {{ productStore.productsLoading ? "Загрузка..." : "Обновить" }}
                    </button>

                    <button class="btn" @click="addProductRow">+ Добавить сотрудника</button>
                </div>
            </div>

            <!--            <p v-if="staffError" class="error">{{ staffError }}</p>-->

            <div class="table">
                <div class="table-row table-row-product table-row-head">
                    <div>ID</div>
                    <div>Брэнд</div>
                    <div>Категория</div>
                    <div>Описание</div>
                    <div>Объем</div>
                    <div>Цена</div>
                    <div>Остаток</div>
                    <div>Фото (url)</div>
                    <div></div>
                </div>

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
                        <input class="input" v-model="p.img_id" placeholder="Ссылка на картинку"/>
                    </div>

                    <div class="row-actions">
                        <button class="btn" @click="productStore.deleteProduct(p.product_id)">Удалить</button>
                    </div>

                    <!--                    <div v-if="m.error" class="error table__error">{{ m.error }}</div>-->
                </div>
            </div>
        </section>

        <!-- Excel -->
        <section class="admin-card">
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

                <button class="btn" :disabled="productStore.excelUploading" @click="uploadExcel">
                    {{ productStore.excelUploading ? "Загрузка..." : "Загрузить и обновить" }}
                </button>

                <p v-if="productStore.excelError" class="error">{{ productStore.excelError }}</p>

                <div v-if="productStore.excelResults" class="result">
                    <h3>Результат импорта</h3>
                    <pre>{{ productStore.excelResults }}</pre>
                </div>
            </div>
        </section>
    </main>
</template>

<style scoped>
.admin {
    //margin: 0 auto;
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

.images-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
}

@media (max-width: 980px) {
    .images-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
    }
}

@media (max-width: 520px) {
    .images-grid {
        grid-template-columns: 1fr;
    }
}

.image-item {
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 10px;
    padding: 10px;
}

.image-item__top {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.badge {
    font-size: 12px;
    padding: 4px 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
}

.image-item__preview {
    height: 140px;
    border-radius: 8px;
    overflow: hidden;
    background: rgba(255, 255, 255, 0.05);
    display: flex;
    align-items: center;
    justify-content: center;
}

.image-item__preview img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.placeholder {
    opacity: 0.6;
    font-size: 13px;
}

.image-item__controls {
    margin-top: 10px;
    display: grid;
    gap: 8px;
}

.btn {
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

.btn--secondary {
    opacity: 0.9;
}

.btn--danger {
    background: #c0392b;
    color: white;
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

.table-row-head {
    opacity: 0.7;
    font-size: 13px;
}

.table-row-staff {
    grid-template-columns: 1fr 1fr 1.6fr 1.6fr 110px;
}

.table-row-product {
    grid-template-columns: 0.25fr 0.7fr 1fr 1fr 0.5fr 0.5fr 0.25fr 1fr 110px;
}

@media (max-width: 980px) {
    .table__row {
        grid-template-columns: 1fr;
    }

    .table__row--head {
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

.excel {
    display: grid;
    gap: 10px;
    max-width: 520px;
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