export function useApiGetters() {
    const {$api} = useNuxtApp()

    function apiUploadPhotos(data) {
        return $api.post('/admin/staff/upload-photos', data)
    }

    function fetchAllStaff() {
        return $api.get('/staff/all')
    }

    function apiAddStaff(data) {
        return $api.post('/admin/staff/add', data)
    }

    function apiChangeStaff(data) {
        return $api.patch('/admin/staff/change', data)
    }

    function apiDeleteStaff(data) {
        return $api.delete('/admin/staff/delete', {data})
    }

    function loginAdmin(loginData) {
        return $api.post('/auth/login', loginData)
    }

    function checkLoginAdmin() {
        return $api.get('/auth/check')
    }

    return {
        apiUploadPhotos,
        fetchAllStaff,
        apiAddStaff,
        apiChangeStaff,
        apiDeleteStaff,
        loginAdmin,
        checkLoginAdmin,
    }
}