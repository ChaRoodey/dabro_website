export const useAuthStore = defineStore('auth', () => {
    const isAuthenticated = ref(false)

    async function checkAuth() {
        const { $api } = useNuxtApp()

        try {
            await $api.get('/auth/check')
            isAuthenticated.value = true
            return true
        } catch (e) {
            isAuthenticated.value = false
            return false
        }
    }

    function login() {
        isAuthenticated.value = true
    }

    function logout() {
        isAuthenticated.value = false
    }

    return {
        isAuthenticated,
        checkAuth,
        login,
        logout,
    }
})