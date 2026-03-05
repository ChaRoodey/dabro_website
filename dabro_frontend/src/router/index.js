import {createRouter, createWebHistory} from 'vue-router'
import {checkLoginAdmin} from "@/api/apiGetters.js";


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'index',
            component: () => import('@/pages/index.vue'),
        },
        {
            path: '/shop',
            name: 'shop',
            component: () => import('@/pages/catalog.vue'),
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('@/pages/login.vue'),
        },
        {
            path: '/admin',
            name: 'admin',
            component: () => import('@/pages/adminPanel.vue'),
            meta: {requiresAuth: true},
        },
    ],
})

router.beforeEach(async (to, from, next) => {
    if (to.meta.requiresAuth) {
        try {
            await checkLoginAdmin()
            next()
        } catch {
            next("/login")
        }
    } else {
        next()
    }

})

export default router
