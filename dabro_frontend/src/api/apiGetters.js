import {fastApi} from '@/api/http.js'


export function fetchAllProducts() {
    return fastApi.get('/products/all')
}

export function fetchAllFilters() {
    return fastApi.get('/products/filters')
}

export function fetchFilteredData(params) {
    return fastApi.get('/products/filter', {params})
}

export function apiAddProducts(data) {
    return fastApi.post('/admin/products/add', data)
}

export function apiChangeProducts(data) {
    return fastApi.patch('/admin/products/change', data)
}

export function apiDeleteProduct(data) {
    return fastApi.delete('/admin/products/delete', {data})
}

export function apiUploadProductsExcel(form) {
    return fastApi.post('/admin/products/upload-excel', form, {
        headers: {"Content-Type": "multipart/form-data"},
    })
}

export function apiUploadProductsPhotos(data) {
    return fastApi.post('/admin/products/upload-photos', data)
}

export function fetchAllStaff() {
    return fastApi.get('/staff/all')
}

export function apiAddStaff(data) {
    return fastApi.post('/admin/staff/add', data)
}

export function apiChangeStaff(data) {
    return fastApi.patch('/admin/staff/change', data)
}

export function apiDeleteStaff(data) {
    return fastApi.delete('/admin/staff/delete', {data})
}

export function loginAdmin(loginData) {
    return fastApi.post('/auth/login', loginData)
}

export function checkLoginAdmin() {
    return fastApi.get('/auth/check')
}
