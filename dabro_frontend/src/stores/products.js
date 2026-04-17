import {ref} from 'vue'
import {defineStore} from 'pinia'
import {
    apiAddProducts,
    apiChangeProducts,
    apiDeleteProduct,
    apiUploadProductsExcel,
    fetchAllFilters,
    fetchAllProducts,
    fetchFilteredData
} from "@/api/apiGetters.js";
import {startLenis, stopLenis} from "@/plugins/lenis.js";
import {usePhotosStore} from "@/stores/photos.js";

const PRODUCT_PATCH_FIELDS = [
    "brand",
    "description",
    "size",
    "category",
    "img_url",
    "excel_product_id",
    "cost",
    "items_left",
    "title",
];

function toAddProductPayload(p) {
    return {
        brand: p.brand,
        description: p.description,
        size: p.size,
        category: p.category,
        img_url: p.img_url,
        excel_product_id: p.excel_product_id,
        cost: p.cost,
        items_left: p.items_left,
        title: p.title,
    };
}

function toPatchProductPayload(oldData, newData) {
    const patch = {product_id: newData.product_id};

    for (const field of PRODUCT_PATCH_FIELDS) {
        if (oldData[field] !== newData[field]) {
            patch[field] = newData[field];
        }
    }

    return Object.keys(patch).length > 1 ? patch : null;
}

export const useProductsStore = defineStore('products', () => {
    const allProducts = ref([])
    const allFilters = ref({brands: [], categories: [], min_price: null, max_price: null})

    const initLoading = ref(false)
    const productsLoading = ref(false)
    const productsUploading = ref(false)
    const productsDeleting = ref(false)
    const adminError = ref('')
    const adminSuccess = ref('')
    const filtersLoading = ref(false)

    const validationErrors = ref({})
    const sidebarOpen = ref(false)

    const excelError = ref('')
    const excelFile = ref(null)
    const excelUploading = ref(false)
    const excelResults = ref(null)

    const productsSnapshot = ref(new Map())

    const photosStore = usePhotosStore();

    function getApiErrorMessage(e) {
        console.log('API error:', e)

        if (
            e.code === 'ECONNABORTED' ||
            e.code === 'ERR_NETWORK' ||
            e.message === 'Network Error' ||
            !e.response
        ) {
            return 'Сервер недоступен, попробуйте позже'
        }

        const detail = e.response?.data?.detail

        if (typeof detail === 'string') {
            return detail
        }

        if (typeof detail === 'object' && detail?.message) {
            return detail.message
        }

        return 'Произошла ошибка'
    }

    function openSidebar() {
        sidebarOpen.value = true

        // stopLenis()
        document.body.style.overflow = "hidden"
    }

    function closeSidebar() {
        sidebarOpen.value = false

        document.body.style.overflow = ""
        // startLenis()
    }

    async function shopLoadInit() {
        initLoading.value = true
        adminError.value = ''

        try {
            const [productsRes, filtersRes] = await Promise.all([fetchAllProducts(), fetchAllFilters(),])
            allProducts.value = productsRes.data.sort((a, b) => b.items_left - a.items_left);
            allFilters.value = filtersRes.data
        } catch (e) {
            adminError.value = getApiErrorMessage(e);
        } finally {
            initLoading.value = false
        }
    }

    async function loadProducts() {
        productsLoading.value = true
        adminError.value = ''

        try {
            const res = await fetchAllProducts();
            allProducts.value = res.data

            const map = new Map()
            for (const item of res.data) {
                map.set(item.product_id, {
                    brand: item.brand ?? null,
                    title: item.title ?? null,
                    description: item.description ?? null,
                    size: item.size ?? null,
                    category: item.category ?? null,
                    img_url: item.img_url ?? null,
                    excel_product_id: item.excel_product_id ?? null,
                    cost: item.cost ?? null,
                    items_left: item.items_left ?? null,
                })
            }
            productsSnapshot.value = map;
        } catch (e) {
            adminError.value = getApiErrorMessage(e);
        } finally {
            productsLoading.value = false
        }
    }

    const loadFilters = async function () {
        filtersLoading.value = true
        try {
            const res = await fetchAllFilters();
            allFilters.value = res.data;
        } finally {
            filtersLoading.value = false
        }
    }

    const loadFilteredData = async function (filters) {
        validationErrors.value = {}
        productsLoading.value = true
        try {
            const res = await fetchFilteredData(filters);
            allProducts.value = res.data.sort((a, b) => b.items_left - a.items_left);
        } catch (e) {
            if (e.response?.status === 422) {
                validationErrors.value = e.response.data.detail
            }
        } finally {
            productsLoading.value = false
        }
    }

    async function uploadProducts() {
        productsUploading.value = true
        adminError.value = ''
        adminSuccess.value = ''

        try {
            const updatedPhotos = await photosStore.uploadPhotos('product')

            if (updatedPhotos) {
                const updatedPhotosMap = new Map(
                    updatedPhotos.map(item => [item.id, item.img_url])
                )

                allProducts.value.forEach(product => {
                    const newUrl = updatedPhotosMap.get(product.product_id)
                    if (newUrl) {
                        product.img_url = newUrl
                    }
                })
            }

            const newItems = [];
            const changedItems = [];

            for (const item of allProducts.value) {
                const oldData = productsSnapshot.value.get(item.product_id)

                if (!oldData) {
                    newItems.push(toAddProductPayload(item));
                    continue;
                }

                const patch = toPatchProductPayload(oldData, item)
                if (patch) changedItems.push(patch)
            }

            if (!newItems.length && !changedItems.length) return

            const results = await Promise.all([
                newItems.length ? apiAddProducts(newItems) : Promise.resolve(),
                changedItems.length ? apiChangeProducts(changedItems) : Promise.resolve()
            ])

            await loadProducts();
            adminSuccess.value = 'Сохранено'
        } catch (e) {
            adminError.value = getApiErrorMessage(e);
        } finally {
            productsUploading.value = false
        }
    }

    async function deleteProduct(id) {
        adminError.value = ''
        productsDeleting.value = true
        adminSuccess.value = ''

        try {
            await apiDeleteProduct({product_id: id})
            await loadProducts()
            adminSuccess.value = 'Удалено'
        } catch (e) {
            adminError.value = getApiErrorMessage(e);
        } finally {
            productsDeleting.value = false
        }
    }

    const uploadProductsExcel = async function () {
        excelResults.value = null;
        if (!excelFile.value) {
            excelError.value = "Выберите Excel файл";
            return;
        }

        excelUploading.value = true;
        try {
            const form = new FormData();
            form.append("file", excelFile.value);

            const res = await apiUploadProductsExcel(form);
            excelResults.value = res.data;
        } catch (e) {
            const detail = e.response?.data?.detail;

            if (detail && typeof detail === 'object') {
                excelResults.value = detail;
                excelError.value = '';
            } else {
                excelResults.value = null;
                excelError.value = detail || "Ошибка импорта";
            }
        } finally {
            excelUploading.value = false;
        }
    }

    return {
        allProducts,
        allFilters,
        initLoading,
        productsLoading,
        productsDeleting,
        adminSuccess,
        filtersLoading,
        adminError,
        validationErrors,
        sidebarOpen,
        excelError,
        excelFile,
        excelUploading,
        excelResults,
        loadProducts,
        loadFilters,
        shopLoadInit,
        loadFilteredData,
        openSidebar,
        closeSidebar,
        uploadProductsExcel,
        uploadProducts,
        deleteProduct,
        getApiErrorMessage,
    }
})
