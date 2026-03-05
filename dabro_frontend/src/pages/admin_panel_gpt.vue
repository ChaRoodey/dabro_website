<script setup>
import {onMounted, ref} from "vue";
import {fastApi} from "@/api/http.js";

// --- state ---
const loadingStaff = ref(false);
const staff = ref([]); // [{id, name, role, phone, photo_url, ...}]
const staffError = ref("");

const images = ref(
    Array.from({length: 8}, (_, i) => ({
        key: `image_${i + 1}`, // идентификатор для бэка
        currentUrl: "",        // текущая картинка с сервера
        file: null,            // новый файл
        previewUrl: "",        // превью
        saving: false,
        error: "",
    }))
);

const excelFile = ref(null);
const excelUploading = ref(false);
const excelResult = ref(null);
const excelError = ref("");

// --- API helpers (поменяй под свои ручки) ---
async function fetchStaff() {
    staffError.value = "";
    loadingStaff.value = true;
    try {
        const res = await fastApi.get("/admin/staff"); // GET список сотрудников
        staff.value = res.data;
    } catch (e) {
        staffError.value = "Не удалось загрузить сотрудников";
    } finally {
        loadingStaff.value = false;
    }
}

async function fetchImages() {
    // Ожидается ответ вида: [{key: "image_1", url:"..."}, ...]
    try {
        const res = await fastApi.get("/admin/images");
        const map = new Map(res.data.map((x) => [x.key, x.url]));
        images.value = images.value.map((img) => ({
            ...img,
            currentUrl: map.get(img.key) || "",
        }));
    } catch (e) {
        // можно показать уведомление, но не критично
    }
}

// --- Images ---
function onPickImageFile(idx, file) {
    const item = images.value[idx];
    item.error = "";

    if (!file) {
        item.file = null;
        item.previewUrl = "";
        return;
    }

    // простая проверка
    if (!file.type.startsWith("image/")) {
        item.error = "Нужен файл изображения";
        return;
    }
    if (file.size > 5 * 1024 * 1024) {
        item.error = "Файл слишком большой (макс 5MB)";
        return;
    }

    item.file = file;
    item.previewUrl = URL.createObjectURL(file);
}

async function saveImage(idx) {
    const item = images.value[idx];
    item.error = "";

    if (!item.file) {
        item.error = "Выберите файл";
        return;
    }

    item.saving = true;
    try {
        const form = new FormData();
        form.append("key", item.key);
        form.append("file", item.file);

        // POST /admin/images/upload (пример)
        const res = await fastApi.post("/admin/images/upload", form, {
            headers: {"Content-Type": "multipart/form-data"},
        });

        // допустим, бэк возвращает url новой картинки
        item.currentUrl = res.data.url;
        item.file = null;
        item.previewUrl = "";
    } catch (e) {
        item.error = "Не удалось сохранить";
    } finally {
        item.saving = false;
    }
}

// --- Staff CRUD (примерно) ---
function addStaffRow() {
    staff.value.unshift({
        id: null,
        name: "",
        role: "",
        phone: "",
        photo_url: "",
        isNew: true,
        saving: false,
        error: "",
    });
}

async function saveStaffMember(member) {
    member.error = "";
    member.saving = true;
    try {
        if (member.id == null) {
            // create
            const res = await fastApi.post("/admin/staff", {
                name: member.name,
                role: member.role,
                phone: member.phone,
                photo_url: member.photo_url,
            });
            Object.assign(member, res.data, {isNew: false});
        } else {
            // update
            await fastApi.patch(`/admin/staff/${member.id}`, {
                name: member.name,
                role: member.role,
                phone: member.phone,
                photo_url: member.photo_url,
            });
        }
    } catch (e) {
        member.error = "Ошибка сохранения";
    } finally {
        member.saving = false;
    }
}

async function deleteStaffMember(member) {
    member.error = "";
    if (member.id == null) {
        // локально удалить несохранённую строку
        staff.value = staff.value.filter((x) => x !== member);
        return;
    }

    try {
        await fastApi.delete(`/admin/staff/${member.id}`);
        staff.value = staff.value.filter((x) => x.id !== member.id);
    } catch (e) {
        member.error = "Не удалось удалить";
    }
}

// --- Excel import ---
function onPickExcel(file) {
    excelError.value = "";
    excelResult.value = null;

    if (!file) {
        excelFile.value = null;
        return;
    }
    const okExt =
        file.name.toLowerCase().endsWith(".xlsx") || file.name.toLowerCase().endsWith(".xls");
    if (!okExt) {
        excelError.value = "Нужен файл .xlsx/.xls";
        return;
    }
    excelFile.value = file;
}

async function uploadExcel() {
    excelError.value = "";
    excelResult.value = null;

    if (!excelFile.value) {
        excelError.value = "Выберите Excel файл";
        return;
    }

    excelUploading.value = true;
    try {
        const form = new FormData();
        form.append("file", excelFile.value);

        // POST /admin/import/products
        const res = await fastApi.post("/admin/import/products", form, {
            headers: {"Content-Type": "multipart/form-data"},
        });

        excelResult.value = res.data; // например {updated, created, skipped, errors:[]}
    } catch (e) {
        excelError.value = "Ошибка импорта";
    } finally {
        excelUploading.value = false;
    }
}

onMounted(async () => {
    await Promise.all([fetchStaff(), fetchImages()]);
});
</script>

<template>
    <main class="admin">
        <header class="admin__header">
            <h1 class="admin__title">Админ-панель</h1>
            <p class="admin__subtitle">Картинки, сотрудники, импорт товаров из Excel</p>
        </header>

        <!-- Images -->
        <section class="card">
            <div class="card__head">
                <h2>Картинки сайта (8 шт.)</h2>
                <p class="muted">Выберите файл → проверьте превью → нажмите “Сохранить”</p>
            </div>

            <div class="images-grid">
                <div class="image-item" v-for="(img, idx) in images" :key="img.key">
                    <div class="image-item__top">
                        <div class="badge">{{ img.key }}</div>
                    </div>

                    <div class="image-item__preview">
                        <img v-if="img.previewUrl" :src="img.previewUrl" alt=""/>
                        <img v-else-if="img.currentUrl" :src="img.currentUrl" alt=""/>
                        <div v-else class="placeholder">Нет картинки</div>
                    </div>

                    <div class="image-item__controls">
                        <input
                                type="file"
                                accept="image/*"
                                @change="onPickImageFile(idx, $event.target.files?.[0] || null)"
                        />

                        <button class="btn" :disabled="img.saving" @click="saveImage(idx)">
                            {{ img.saving ? "Сохранение..." : "Сохранить" }}
                        </button>

                        <p v-if="img.error" class="error">{{ img.error }}</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- Staff -->
        <section class="card">
            <div class="card__head staff-head">
                <h2>Сотрудники</h2>

                <div class="staff-actions">
                    <button class="btn btn--secondary" @click="fetchStaff" :disabled="loadingStaff">
                        {{ loadingStaff ? "Загрузка..." : "Обновить" }}
                    </button>
                    <button class="btn" @click="addStaffRow">+ Добавить сотрудника</button>
                </div>
            </div>

            <p v-if="staffError" class="error">{{ staffError }}</p>

            <div class="table">
                <div class="table__row table__row--head">
                    <div>Имя</div>
                    <div>Должность</div>
                    <div>Телефон</div>
                    <div>Фото (url)</div>
                    <div></div>
                </div>

                <div class="table__row" v-for="m in staff" :key="m.id ?? m._tmpKey ?? m.name">
                    <div>
                        <input class="input" v-model="m.name" placeholder="Имя"/>
                    </div>
                    <div>
                        <input class="input" v-model="m.role" placeholder="Должность"/>
                    </div>
                    <div>
                        <input class="input" v-model="m.phone" placeholder="+7..."/>
                    </div>
                    <div>
                        <input class="input" v-model="m.photo_url" placeholder="https://..."/>
                    </div>

                    <div class="row-actions">
                        <button class="btn" :disabled="m.saving" @click="saveStaffMember(m)">
                            {{ m.saving ? "..." : "Сохранить" }}
                        </button>
                        <button class="btn btn--danger" @click="deleteStaffMember(m)">Удалить</button>
                    </div>

                    <div v-if="m.error" class="error table__error">{{ m.error }}</div>
                </div>
            </div>
        </section>

        <!-- Excel -->
        <section class="card">
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

                <button class="btn" :disabled="excelUploading" @click="uploadExcel">
                    {{ excelUploading ? "Загрузка..." : "Загрузить и обновить" }}
                </button>

                <p v-if="excelError" class="error">{{ excelError }}</p>

                <div v-if="excelResult" class="result">
                    <h3>Результат импорта</h3>
                    <pre>{{ excelResult }}</pre>
                </div>
            </div>
        </section>
    </main>
</template>

<style scoped>
.admin {
    max-width: 1100px;
    margin: 0 auto;
    padding: 24px 16px 60px;
}

.admin__header {
    margin-bottom: 18px;
}

.admin__title {
    font-size: 28px;
    margin: 0 0 6px;
}

.admin__subtitle {
    margin: 0;
    opacity: 0.75;
}

.card {
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
    height: 38px;
    padding: 0 12px;
    border-radius: 10px;
    border: 0;
    cursor: pointer;
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

.table__row {
    display: grid;
    grid-template-columns: 1.2fr 1fr 1fr 1.6fr 220px;
    gap: 8px;
    align-items: center;
}

.table__row--head {
    opacity: 0.7;
    font-size: 13px;
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