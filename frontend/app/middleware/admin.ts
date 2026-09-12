export default defineNuxtRouteMiddleware(async () => {
    const authStore = useAuthStore()

    const authenticated = await authStore.checkAuth()

    if (!authenticated) {
        return navigateTo('/login')
    }
})