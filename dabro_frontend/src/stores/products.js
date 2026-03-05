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

const PRODUCT_PATCH_FIELDS = [
    "brand",
    "description",
    "size",
    "category",
    "img_id",
    "excel_product_id",
    "cost",
    "items_left"
];

function toAddProductPayload(p) {
    return {
        brand: p.brand,
        description: p.description,
        size: p.size,
        category: p.category,
        img_id: p.img_id,
        excel_product_id: p.excel_product_id,
        cost: p.cost,
        items_left: p.items_left,
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
    const filtersLoading = ref(false)
    const error = ref(null)
    const validationErrors = ref({})
    const sidebarOpen = ref(false)
    const excelError = ref('')
    const excelFile = ref(null)
    const excelUploading = ref(false)
    const excelResults = ref(null)
    const productsSnapshot = ref(new Map())

    function openSidebar() {
        sidebarOpen.value = true

        stopLenis()
        document.body.style.overflow = "hidden"
    }

    function closeSidebar() {
        sidebarOpen.value = false

        startLenis()
        document.body.style.overflow = ""
    }

    async function shopLoadInit() {
        initLoading.value = true
        error.value = false

        try {
            const [productsRes, filtersRes] = await Promise.all([fetchAllProducts(), fetchAllFilters(),])
            allProducts.value = productsRes.data
            allFilters.value = filtersRes.data
        } catch (e) {
            error.value = e
        } finally {
            initLoading.value = false
        }
    }

    async function loadProducts() {
        productsLoading.value = true
        try {
            const res = await fetchAllProducts();
            allProducts.value = res.data;

            const map = new Map()
            for (const item of res.data) {
                map.set(item.product_id, {
                    brand: item.brand ?? "",
                    description: item.description ?? "",
                    size: item.size ?? "",
                    category: item.category ?? "",
                    img_id: item.img_id ?? "",
                    excel_product_id: item.excel_product_id ?? null,
                    cost: item.cost ?? null,
                    items_left: item.items_left ?? null,
                })
            }
            productsSnapshot.value = map;
        } finally {
            productsLoading.value = false
        }
    }

    const loadFilters = async function () {
        filtersLoading.value = true
        try {
            const res = await fetchAllFilters();
            allFilters.value = res.data;
            // console.log(allFilters.value);
        } finally {
            filtersLoading.value = false
        }
    }

    const loadFilteredData = async function (filters) {
        validationErrors.value = {}
        productsLoading.value = true
        // console.log(filters);
        try {
            const res = await fetchFilteredData(filters);
            allProducts.value = res.data;
            // console.log(allProducts.value);
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

        try {
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

            if (!newItems.length && !changedItems.length) return;

            const results = await Promise.all([
                newItems.length ? apiAddProducts(newItems) : Promise.resolve(),
                changedItems.length ? apiChangeProducts(changedItems) : Promise.resolve()
            ])

            await loadProducts();
        } catch (e) {
            console.log(e);
        } finally {
            productsUploading.value = false
        }
    }

    async function deleteProduct(id) {
        try {
            await apiDeleteProduct({product_id: id})
            await loadProducts()
        } catch (e) {
            console.log(e);
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
            excelError.value = e.response?.data?.detail ?? "Ошибка импорта";
        } finally {
            excelUploading.value = false;
        }
    }

    return {
        allProducts,
        allFilters,
        initLoading,
        productsLoading,
        filtersLoading,
        error,
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
    }
})
